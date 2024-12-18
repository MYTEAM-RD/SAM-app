from app.auth_wrapper import token_required
from app.email import Email_with_template
from app.models.analyse import Analyse
from app.models.verification import Verification
from app.user import bp
from app.models.user import User
from app.extensions import db
from flask import request, current_app, jsonify, redirect
import stripe
import os
import json


@bp.route("/create_payment", methods=["POST"])
@token_required
def create_payment_checkout(token):
    user = User.query.filter_by(id=token["id"]).first_or_404()
    try:
        data = request.get_json()
        subscription = False
        stripe_item_list = []
        sam_item_list = []
        for item in data["items"]:
            curent_subscription = False
            stripe_item = stripe.Product.retrieve(item["id"])
            stripe_item_list.append(
                {
                    "price": stripe_item.get("default_price"),
                    "quantity": item.get("quantity", 1),
                }
            )
            if "subscription_credit" in stripe_item["metadata"]:
                curent_subscription = True
            sam_item_list.append(
                {
                    "id": stripe_item.get("id"),
                    "quantity": item.get("quantity", 1),
                    "type": "payment" if not curent_subscription else "subscription",
                    "amount": int(stripe_item["metadata"].get("credit", 0))
                    + int(stripe_item["metadata"].get("subscription_credit", 0)),
                }
            )
            if curent_subscription:
                subscription = True
        verification = Verification(
            user_id=user.id, type="payment", note=json.dumps(sam_item_list)
        )
        checoukt_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=stripe_item_list,
            mode="subscription" if subscription else "payment",
            success_url=os.environ.get("SUCCESS_URL"),
            cancel_url=data.get("cancel_url", os.environ.get("CANCEL_URL")),
            client_reference_id=token.get("id"),
            customer=user.get_customer_id(),
            invoice_creation=None
            if subscription
            else {
                "enabled": True,
            },
        )
        return checoukt_session.url, 200
    except Exception as e:
        current_app.logger.error(e)
        return "Invalid json", 400


@bp.route("/products", methods=["GET"])
def get_products():
    try:
        product_list = stripe.Product.list()
        for item in product_list["data"]:
            item["price"] = stripe.Price.retrieve(item["default_price"])
    except Exception as e:
        current_app.logger.error(e)
        return "Internal server error, payment provider unavaible", 500
    return jsonify(product_list), 200


@bp.route("/price/<id>", methods=["GET"])
def get_price(id):
    try:
        price = stripe.Price.retrieve(id)
    except Exception as e:
        current_app.logger.error(e)
        return "Internal server error, payment provider unavaible", 500
    return jsonify(price), 200


@bp.route("/customer_portal", methods=["GET"])
@token_required
def get_customer_portal(token):
    user = User.query.filter_by(id=token["id"]).first_or_404()
    try:
        session = stripe.billing_portal.Session.create(
            customer=user.get_customer_id(),
            return_url=os.environ.get("FRONTEND_URL")+"/account",
        )
    except Exception as e:
        current_app.logger.error(e)
        return "Internal server error, payment provider unavaible", 500
    return jsonify(session), 200


@bp.route("/sucess_payment/<id>/", methods=["GET"])
def sucess_payment(id):
    verfification = Verification.query.filter_by(id=id).first_or_404()
    user = User.query.filter_by(id=verfification.user_id).first_or_404()
    try:
        note = json.loads(verfification.note)
        for item in note:
            if item["type"] == "payment":
                user.credit += int(item["amount"]) * int(item.get("quantity", 1))
        db.session.commit()
        db.session.delete(verfification)
        db.session.commit()
        return redirect(
            request.args.get("redirect_url", os.environ.get("FRONTEND_URL")), code=302
        )
    except Exception as e:
        current_app.logger.error(e)
        return "Internal server error, payment provider unavaible", 500


@bp.route("/webhook", methods=["POST"])
def webhook():
    # add subscription to user linked with customer id in stripe using invoice.payment_succeeded
    event = None
    payload = request.data
    sig_header = request.headers["STRIPE_SIGNATURE"]
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.environ.get("STRIPE_WEBHOOK_SECRET")
        )
    except ValueError as e:
        # Invalid payload
        current_app.logger.error(e)
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        current_app.logger.error(e)
        return "Invalid signature", 400
    # Handle the event
    if event["type"] == "invoice.payment_succeeded":
        invoice = event["data"]["object"]
        for item in invoice["lines"]["data"]:
            if item["type"] == "subscription":
                user = User.query.filter_by(
                    customer_id=invoice["customer"]
                ).first_or_404()
                product = stripe.Product.retrieve(item["price"]["product"])
                a = product["metadata"].get("subscription_credit", 0)
                b = item["quantity"]
                user.add_n_subscription_credit(int(a) * int(b))
            if item["type"] == "invoiceitem":
                user = User.query.filter_by(
                    customer_id=invoice["customer"]
                ).first_or_404()
                product = stripe.Product.retrieve(item["price"]["product"])
                user.credit = str(int(user.credit) + int(product["metadata"].get("credit", 0)) * int(
                    item["quantity"]
                ))
    else:
        return jsonify(success=True), 200
    db.session.commit()
    return jsonify(success=True), 200
