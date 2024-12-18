import Paper from '@mui/material/Paper';
import MenuList from '@mui/material/MenuList';
import MenuItem from '@mui/material/MenuItem';
import ListItemText from '@mui/material/ListItemText';
import ListItemIcon from '@mui/material/ListItemIcon';
import DeleteForeverIcon from '@mui/icons-material/DeleteForever';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import SimCardDownloadIcon from '@mui/icons-material/SimCardDownload';
import Snackbar from '@mui/material/Snackbar';
import Alert from '@mui/material/Alert';
import { useEffect, useRef, useState } from 'react';
import { backendUrl } from '../../utils/var';
import useCookie from 'react-use-cookie';

export default function ModalMenu({ show, close, index , item}) {
  const paperRef = useRef(null);
  // eslint-disable-next-line
  const [token, setToken] = useCookie('token', "")
  const [open, setOpen] = useState(false);

  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setOpen(false);
  };

  function downloadFile(e,items) {
    e.stopPropagation();
    fetch(`${backendUrl}/api/v1/analyse/${items.id}`, {
      method: 'GET',
      headers: {
        "Authorization": "Bearer " + token
      }
    })
    .then(response => response.blob())
      .then(blob => {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = items.filename;
        document.body.appendChild(a);
        a.click();
        a.remove();
        URL.revokeObjectURL(url);
      })
      .catch(error => console.error(error));
  }

  function deleteProject(e,items) {
    e.stopPropagation();
    fetch(`${backendUrl}/api/v1/analyse/${items.id}`, {
      method: 'DELETE',
      headers: {
        "Authorization": "Bearer " + token
      }
    }).then(response => {
      window.location.reload();
    })
      .catch(error => console.error(error));
  }

  useEffect(() => {
    function handleClickOutside(event) {
      if (paperRef.current && !paperRef.current.contains(event.target)) {
        close(index);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [close, index]);

  if (show) {
    return (
      <>
      <Paper sx={{ width: 230, maxWidth: '100%' }} style={{ position: 'absolute', transform: "translateX(-200px)" }} ref={paperRef}>
        <MenuList>
          <MenuItem onClick={(e)=>{downloadFile(e,item)}}>
            <ListItemIcon>
              <FileDownloadIcon fontSize="small" />
            </ListItemIcon>
            <ListItemText>Telecharger le projet</ListItemText>
          </MenuItem>
          <MenuItem onClick={(e)=>{e.stopPropagation();setOpen(true)}}>
            <ListItemIcon>
              <SimCardDownloadIcon fontSize="small" />
            </ListItemIcon>
            <ListItemText>Telecharger un rapport</ListItemText>
          </MenuItem>
          <MenuItem onClick={(e)=>{deleteProject(e,item)}}>
            <ListItemIcon>
              <DeleteForeverIcon fontSize="small" />
            </ListItemIcon>
            <ListItemText>Effacer l'analyse</ListItemText>
          </MenuItem>
        </MenuList>
      </Paper>
      <Snackbar open={open} autoHideDuration={4000} onClose={handleClose}>
      <Alert onClose={handleClose} severity="error" sx={{ width: '100%' }}>
        Cette fonctionnalité n'est pas encore disponible
      </Alert>
    </Snackbar>
    </>
    );
  } else {
    return null;
  }
}
