function createBox(name, date, patient, id) {
    let card = document.createElement('div');
    card.classList.add('card');
    let img = document.createElement('img');
    img.src = "https://cdn-icons-png.flaticon.com/512/822/822118.png";
    img.style.width = "15%"; img.style.height = "auto"; img.style.float = "left";
    // card body
    let body = document.createElement('div');
    body.classList.add('card-body'); body.style.float = "left";
    let bodyTitle = document.createElement('h4');
    bodyTitle.classList.add('card-title'); bodyTitle.classList.add('text-center');
    bodyTitle.innerText = name;
    let bodyText = document.createElement('p');
    bodyText.classList.add('card-text');
    bodyText.innerText = date; bodyText.style.display = 'inline-block'; bodyText.style.margin = '10px';
    let bodyLink = document.createElement('a');
    bodyLink.classList.add('text-white'); bodyLink.classList.add('mybtn');  bodyLink.classList.add('main-color');
    bodyLink.innerText = "查看分析";
    bodyLink.style.margin = '10px';
    bodyLink.href = "/analysis/" + id;
    let dataAndBtn = document.createElement('div');
    dataAndBtn.appendChild(bodyText); dataAndBtn.appendChild(bodyLink);

    // append child
    body.appendChild(img);
    body.appendChild(bodyTitle);
    //body.appendChild(bodyText);
    body.appendChild(dataAndBtn);

    card.appendChild(body);
    card.style.margin = "30px";
    return card;
}
window.onload = function() {
    const url = '/api/public_record';
    fetch(url, {
      method:'POST',
      body: JSON.stringify({
         name: document.getElementById('user-name').innerText
     }),
     headers: {
        'Content-Type': 'hello; charset=utf-8'
     }
    })
    .then(res => res.json())  // 使用 json() 可以得到 json 物件
    .catch(error => console.error('Error:', error))
    .then(response => {
        console.log('Success:', response);
        // show them
        if (response.items.length != 0) {
            // show them
            for (let i = 0; i < response.items.length; i++) {
                let item = createBox(response.items[i].name, response.items[i].date, response.items[i].patient, response.items[i].id);
                let recordContainer = document.getElementById('record-container');
                recordContainer.appendChild(item);
            }
        } else {
            // empty
            // prompt upload button
            let recordContainer = document.getElementById('record-container');
            let emptyContent = createEmptyContent();
            recordContainer.appendChild(emptyContent);
        }
    });
}
