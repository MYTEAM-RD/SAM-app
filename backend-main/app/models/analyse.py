from app.extensions import db
from cryptography.fernet import Fernet
import datetime
import uuid
import os
from ..ai.process import (
    import_and_predict,
    process_prob_cir,
    read_file,
    process_montant_pred,
)
import io


class Analyse(db.Model):
    id = db.Column(db.Text, primary_key=True)
    filename = db.Column(db.Text, unique=False, nullable=True)
    file_byte = db.Column(db.LargeBinary, unique=False, nullable=True)
    analyzed = db.Column(db.Boolean, unique=False, default=False)
    analyse_data = db.Column(db.JSON, unique=False, nullable=True)
    budget = db.Column(db.Float, unique=False, nullable=True)
    created_by = db.Column(
        db.Text, db.ForeignKey("user.id"), unique=False, nullable=False
    )
    created_at = db.Column(db.DateTime, unique=False, nullable=False)
    updated_at = db.Column(db.DateTime, unique=False, nullable=False)

    def __init__(
        self,
        file_byte: bytes,
        created_by: str,
        budget: float = None,
        filename: str = None,
        analyzed: bool = False,
        analyse_data: dict = None,
        created_at=datetime.datetime.utcnow(),
        id=None,
    ):
        f = Fernet(os.environ.get("FRENET_KEY"))

        self.id = id if id is not None else str(uuid.uuid4())
        self.created_by = created_by
        self.filename = filename
        self.file_byte = f.encrypt(file_byte)
        self.budget = budget
        self.analyzed = analyzed
        self.analyse_data = analyse_data
        self.created_at = created_at
        self.updated_at = created_at
        self.last_login = created_at

    def get_file(self) -> bytes:
        f = Fernet(os.environ.get("FRENET_KEY"))
        return f.decrypt(self.file_byte)

    def set_file(self, file_byte: bytes) -> None:
        f = Fernet(os.environ.get("FRENET_KEY"))
        self.file_byte = f.encrypt(file_byte)

    def run_analyse(self) -> None:
        """Run the analysis on the provided file.

        Raises:
            ValueError: If the file is empty.

        Notes:
            This method initializes the 'analyse_data' dictionary and populates it with the results of the analysis.
            It extracts the raw texts from the file, performs predictions, and stores the analysis results in 'analyse_data'.

        Example:
            analyse = Analyse(...)
            analyse.run_analyse()
        """
        if self.file_byte is None:  # Check if the file is empty
            raise ValueError("File is empty")

        self.analyse_data = {}  # Initialize the 'analyse_data' dictionary
        self.analyse_data[
            "project_list"
        ] = []  # Initialize the list of projects in 'analyse_data'

        name = self.filename.split(".")[0]  # Extract the name from the filename

        buffer = io.BytesIO()  # Create a buffer to read the file content
        buffer.name = self.filename
        buffer.write(self.get_file())  # Write the file content to the buffer
        buffer.seek(0)

        raw_texts_list_, technical_part_detected_ = read_file(
            buffer
        )  # Read the file and detect technical parts

        self.analyse_data[
            "technical_part_detected_"
        ] = technical_part_detected_  # Store technical part detection result

        for j, text in enumerate(raw_texts_list_):  # Iterate over the raw texts
            project_name = name
            if (
                len(raw_texts_list_) > 1
            ):  # If there are multiple texts, append project number to the project name
                project_name += " - Projet " + str(j + 1)

            self.analyse_data["project_list"].append(
                {
                    "project_name": project_name,
                }
            )  # Create a dictionary for each project and add it to the 'project_list'

            prob_cir_, montant_pred_ = import_and_predict(raw_text=text)[
                0
            ]  # Perform predictions on the text

            self.analyse_data["project_list"][j]["result"] = process_prob_cir(
                prob_cir_
            )  # Process the prediction results
            self.analyse_data["project_list"][j]["montant_pred_"] = int(
                montant_pred_
            )  # Store the predicted amount
            self.analyse_data["project_list"][j]["budget"] = None  # Store the raw text

        self.analyzed = True  # Set the 'analyzed' flag to True to indicate that analysis has been performed

    def estimate(self, budget: float, index: int) -> bool:
        if self.analyse_data is None:
            raise ValueError("Analyse is empty")
        if self.analyzed == False:
            raise ValueError("Analyse is not finished")
        self.analyse_data["project_list"][index]["budget"] = budget
        from sqlalchemy.orm.attributes import flag_modified  
        flag_modified(self, "analyse_data")
        return process_montant_pred(
            int(self.analyse_data["project_list"][index]["montant_pred_"]), int(budget)
        )

    def generate_report(self) -> bytes:
        # replace the following line with your code to generate the report
        return b"test"

    def public_json(self) -> dict:
        return {
            "id": self.id,
            "filename": self.filename,
            "analyzed": self.analyzed,
            "analyse_data": self.analyse_data,
            "budget": self.budget,
            "created_at": self.created_at.timestamp(),
            "updated_at": self.updated_at.timestamp(),
        }

    def __repr__(self):
        return f'<Analys "{self.id}">'
