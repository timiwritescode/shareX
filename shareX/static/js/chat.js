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