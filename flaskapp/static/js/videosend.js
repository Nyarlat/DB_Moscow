

let video

function handleFileChange(event) {
    let fileNameDisplay = document.getElementById('filetext');
    let fileInput = event.target;
    video = fileInput.files[0];

    console.log(video.name);

    if (video) {

        document.getElementById("filetext").textContent = video.name;

        block_info();
    } else {
        fileNameDisplay.textContent = '';
    }
}


function block_info() {

    document.getElementById("info_container").innerHTML = `
    <div class="block block_info">
                <h2 class="block__h block_info__h">Генерация тэгов</h1>
                <div class="block_info__separetor"></div>
                <div class="block_info__row">
                    <div class="block_info__column">
                        <div>
                            <h3 class="block_info__column__h3">Название видео:</h3>
                            <input class="main__entry__input"  type="text"  placeholder="Название..." id="videoname">
                        </div>
                        <div>
                            <h3 class="block_info__column__h3">Описание видео:</h3>
                            <textarea class="main__entry__text" type="text" id="description" oninput="autoResize()"  placeholder="Описание..."></textarea>
                        </div>
                        <div>
                            <button class="main__entry__button" id="send_link_btn" onclick="videoSend()">
                                Сгенерировать теги
                            </button>
                        </div>
                    </div>
                    <div>
                        <video class="block_info__video" src="" id="videoPlayer"  controls></video>
                    </div>
                </div>
            </div>
    `;


    const videoPlayer = document.getElementById('videoPlayer');

    const fileURL = URL.createObjectURL(video);  // Создаем URL для файла
    videoPlayer.src = fileURL;  // Устанавливаем видео на проигрыватель
    videoPlayer.load();
}





function videoSend() {

    // Получаем элементы, например, из формы или других источников
    let text1 = document.querySelector('#videoname').value;          // первая строка текста
    let text2 = document.querySelector('#description').value;          // вторая строка текста

    // Создаем объект FormData
    const formData = new FormData();
    formData.append('video', video);  // добавляем видеофайл
    formData.append('text1', text1);      // добавляем первую строку текста
    formData.append('text2', text2);      // добавляем вторую строку текста


    // Отправляем данные на сервер с помощью fetch
    fetch('/api/video', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Успех:', data);

        a2t = data["a2t"];
        v2t = data["v2t"];
        cath = data["cath"];
        // acc = data["acc"];
        
        result = `
            <div class="result_2text">
                    <div class="result_2text__column">
                        <h2>Распознанная речь</h3>
                        <div class="result_2text__text">
                        `+ a2t +`
                        </div>
                    </div>
                    <div class="result_2text__column">
                        <h2>Распознанный видеоряд</h3>
                        <div class="result_2text__text">
                        `+ v2t +`
                        </div>
                    </div>
                </div>

            <div class="block_result" id="block_result">
                <h2>Подходящие тэги</h2>
                <div class="block_result__container">
                    <div class="block_result__separator"></div>
                    <div class="block_result__list">
                    `;


        for (i in cath){
            result += `
                <div class="block_result__list_item">
                    <div>
                        `+ cath[i] +`
                    </div>
                </div>
            `
        };
        // for (i in cath){
        //     result += `
        //         <div class="block_result__list_item">
        //             <div>
        //                 `+ cath[i] +`
        //             </div>
        //             <div>
        //                 `+ acc[i] +`
        //             </div>
        //         </div>
        //     `
        // };
                        

        result += `
                    </div>
                </div>
            </div>
        `;

        document.getElementById("result_container").innerHTML = result;

    })
    .catch((error) => {
        console.error('Ошибка:', error);
    });
}