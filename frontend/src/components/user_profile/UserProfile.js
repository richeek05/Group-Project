import '../../../node_modules/bootstrap/dist/css/bootstrap.min.css';
import React, { useState,useEffect } from 'react';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import axios from "axios";
import Card from 'react-bootstrap/Card';
import EditProfile from './EditProfile';



function UserProfile(props) {
    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    const [authorToDisplay, setAuthorToDisplay] = useState(props.author);
  
    const handleAuthorView = () => {
      axios.get( props.author.id)
      //.then((response) => {setComments(response.data.comments[0].comment);})
      .then((response) => {console.log(response.data.author) ;})
      .catch(error => console.log(error));
      }
  
    //var commentView = comments.map((comm) => <Card><Card.Body>{comm.author.displayName}{": "}{comm.comment}</Card.Body></Card>)
    
    


console.log(props.author)
//console.log(author)
return (
    <>
    <Button variant="sucess"  onClick={() => {handleAuthorView();handleShow();}}>
             {authorToDisplay.displayName}
          </Button>

    <Modal show={show} onHide={handleClose} centered>
        <Modal.Header closeButton>
            <Modal.Title>Profile Information</Modal.Title>
        </Modal.Header>
        
    <Modal.Body>

        <p style={{ textAlign: "center" }}> <img src={props.author.profileImage} width="80" height="80" style={ {borderRadius: "20px" }}/></p>
        <p>Display Name: {authorToDisplay.displayName}</p>
        <p>Github: <a href={authorToDisplay.github}> {authorToDisplay.github} </a>  </p>
     

    </Modal.Body>

    <Modal.Footer>

    <EditProfile setAuthorToDisplay={setAuthorToDisplay} authString={props.authString} author={props.author} postContent={props.postObject} setPostItems={props.setPostItems} />

    <Button variant="outline-warning" onClick={handleClose}>
        Close
    </Button>
  
    </Modal.Footer>
    </Modal>
    </>
)

}

export default UserProfile;