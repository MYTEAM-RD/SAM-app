import Snackbar from '@mui/material/Snackbar';
import Alert from '@mui/material/Alert';
import Slide from '@mui/material/Slide';

export default function ModalError({ open, setOpen, text, severity="error"}) {

    function TransitionLeft(props) {
        return <Slide {...props} direction="left" />;
      }

  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setOpen(false);
  };

    return (
    <>
        <Snackbar TransitionComponent={TransitionLeft} anchorOrigin={{ vertical:'bottom', horizontal:'right' }} open={open} autoHideDuration={6000} onClose={handleClose}>
            <Alert onClose={handleClose} severity={severity} sx={{ width: '100%' }}>
                {text}
            </Alert>
        </Snackbar>
    </>
    );
}
