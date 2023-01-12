function createChat(items) {
    let wrapper = document.getElementsByClassName('wrapper')[0];
    let ul = document.createElement('ul');
    for (let i = 0; i < items.length; i++) {
        let li = document.createElement('li');
        li.innerText = items[i].content;
        if (items[i].identity == 'SPEAKER_00') {
            li.classList.add('patient');
            li.classList.add('blank-color');
            li.classList.add('text-black');
        } else {
            li.classList.add('doctor');
            li.classList.add('main-color');
            li.classList.add('text-white');
        }
        ul.appendChild(li);
    }
    wrapper.appendChild(ul);
}
function createAudio(code) {
    let audio = document.getElementsByTagName('audio')[0];
    audio.src = 'data:audio/wav;base64,' + code.substring(2, code.length-1);
}

function loadPage(imageUrl, report) {
    let originPage = document.getElementById('origin-page');
    let visualPage = document.getElementById('visual-page');
    let reportPage = document.getElementById('report-page');
    let visualContent = document.getElementById('visual-content');
    let reportContent = document.getElementById('report-content');
    let originBtn = document.getElementById('origin-btn');
    let visualBtn = document.getElementById('visual-btn');
    let reportBtn = document.getElementById('report-btn');

    // initialize
    visualPage.style.display = "none";
    reportPage.style.display = "none";

    originBtn.onclick = function() {
        originPage.style.display = "block";
        visualPage.style.display = "none";
        reportPage.style.display = "none";
        originBtn.classList.add('blank-color');
        originBtn.style.backgroundColor = "#248888";
        visualBtn.style.backgroundColor = "#E6E6E6";
        reportBtn.style.backgroundColor = "#E6E6E6";
    }
    visualBtn.onclick = function() {
        visualPage.style.display = "block";
        originPage.style.display = "none";
        reportPage.style.display = "none";
        visualBtn.style.backgroundColor = "#248888";
        originBtn.style.backgroundColor = "#E6E6E6";
        reportBtn.style.backgroundColor = "#E6E6E6";
    }
    reportBtn.onclick = function() {
        reportPage.style.display = "block";
        visualPage.style.display = "none";
        originPage.style.display = "none";
        reportBtn.style.backgroundColor = "#248888";
        visualBtn.style.backgroundColor = "#E6E6E6";
        originBtn.style.backgroundColor = "#E6E6E6";
    }
    wordcloud = document.createElement('img');
    wordcloud.src = imageUrl;
    wordcloud.referrerpolicy="no-referrer";
    wordcloud.style.marginTop = "50px";
    visualContent.appendChild(wordcloud);
}

window.onload = function() {
    const url = '/api/chat_record';
    fetch(url, {
      method:'POST',
      body: JSON.stringify({
         name: document.getElementById('user-name').innerText,
         id: document.getElementById('secret').innerText,
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
            createAudio(response.code);
            createChat(response.items);
            loadPage(response.img_url, null);
        } else {
            // empty
            // prompt upload button
            console.log("error");
        }
    });
}
