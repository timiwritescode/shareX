import {month, weekday} from "./date.js"

let homeBtn = document.getElementById('home-btn')
homeBtn.addEventListener('click', navigateToHome)

let dotsBtns = document.querySelectorAll('#dots')
Array.from(dotsBtns).forEach((dotsBtn) => {
    dotsBtn.addEventListener('click', () => {
    const dialogBox = dotsBtn.parentNode.querySelector('#dialog-box')
    if (dialogBox.classList.contains('dialog-box-show')) {
        // show the dialog box
        dialogBox.classList.remove('dialog-box-show')
        // and also hide the text area of the edit message 
        const messageId = dotsBtn.parentNode.attributes['data-message-id'].value
        hideEditInput(+messageId)
    } else {
        dialogBox.classList.add('dialog-box-show')
    }
});
});

const showEditBtns = document.querySelectorAll('#show-edit-btn');
const deleteBtns = document.querySelectorAll('#delete-btn')
const saveEditBtns = document.querySelectorAll('#save-edit-btn')
const hideEditBtns = document.querySelectorAll('#hide-edit-btn')

Array.from(showEditBtns).forEach((showEditBtn) => {
    let messageId = getMessageIdFromClickedButton(showEditBtn)
    showEditBtn.addEventListener('click', ()=> {
        showEditInput(messageId)
    })
});

Array.from(deleteBtns).forEach((deleteBtn)=>{
    let messageId = getMessageIdFromClickedButton(deleteBtn)
    deleteBtn.addEventListener('click', ()=>{
        deleteMessage(messageId);
    })
}) 

Array.from(saveEditBtns).forEach((saveEditBtn)=>{
    let messageId = getMessageIdFromClickedButton(saveEditBtn)
    saveEditBtn.addEventListener('click', ()=>{
        editMessage(messageId);
    })
    
}) 

Array.from(hideEditBtns).forEach((hideEditBtn)=>{
    let messageId = getMessageIdFromClickedButton(hideEditBtn)
    hideEditBtn.addEventListener('click', ()=>{
        hideEditInput(messageId);
    })
}) 

// function to get the message Id of a button clicked of a particular message
function getMessageIdFromClickedButton(button) {
    let messageId = button.attributes['data-message-id'].value
    console.log("message id: "+ messageId)
    return +messageId 
}

function showEditInput(messageId) {
    console.log(messageId)
    const editMessage = document.querySelector(`.edit-container[data-message-id="${messageId}"]`)
    editMessage.classList.add('edit-container-show')
    const editTextArea = editMessage.querySelector('textarea');
    const message = document.querySelector(`.chat-message[data-message-id="${messageId}"]`)
    editTextArea.value = message.querySelector('.message').textContent.trim();
    
}

function hideEditInput(messageId) {
    console.log(messageId)
    const editContainer = document.querySelector(`.edit-container[data-message-id="${messageId}"]`)
    if (editContainer.classList.contains('edit-container-show')) {
        editContainer.classList.remove('edit-container-show')
    }
};    

function editMessage (messageId) {
    const editTextarea = document.querySelector(`#edit-textarea[data-message-id="${messageId}"]`);  
    console.log(editTextarea)
    let editMessageText =  editTextarea.value
    console.log(editMessageText)
    fetch(`/chat/edit_message/${messageId}`, {
        method: "PATCH",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ editMessage: editMessageText })
    })
    .then(response => {
        if (response.ok) {
            const messagecontainer = document.querySelector(`.chat-message[data-message-id="${messageId}"]`);
            const messageTextContent = messagecontainer.querySelector(`.message`);
            messageTextContent.textContent = editTextarea.value;
        }
    }) 
    .catch(error => {
        console.error('Error editing message', error)
    })
};

function deleteMessage(messageId) {
    fetch(`/chat/delete_message/${messageId}`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
    }).then(response => {
        if (response.ok) {
            const messageElement = document.querySelector(`.chat-message[data-message-id="${messageId}"]`)
            if (messageElement) {
                messageElement.remove();
            }
        }
    }).catch(error => {
        console.error('Error deleting message', error);
    });
};

function navigateToHome () {
    window.location.href = '/'
}

// function to get the current date
function getDate() {
    let today = new Date()
    today.setHours(0,0,0,0)
    let currentMonth = today.getMonth() + 1 // javascripts start couting index of month from 0
    let day = today.getDay()   
    let date = today.getDate()
    let year = today.getFullYear()
    currentMonth = month[currentMonth]
    day = weekday[day]
    return `${day}, ${currentMonth} ${date}, ${year}`
}

// function to post date on chat room 
function postDate() {
    let today = getDate()
    const dateElement = document.querySelector(`.date-container[data-date="${getDate()}"]`);
    console.log(dateElement)
    if (!dateElement) {
        createDateElement(today)
    }
    
}

function createDateElement (date) {
    const dateContainer = document.createElement('div');
    dateContainer.classList.add('date-container');
    dateContainer.attributes["data-date"] = date
    dateContainer.textContent = date;
    const messageArea =  document.querySelector('.chat-messages');
    messageArea.appendChild(dateContainer)
}  

postDate()
// window.addEventListener('DOMContentLoaded', postDate)