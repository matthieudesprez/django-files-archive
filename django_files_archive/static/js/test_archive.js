$(function () {
    let jsonForm;

    function initForm() {
        const files = Array(4).fill('https://picsum.photos/200/150');
        for (let i = 0; i < files.length; i++) {
            const rowFile = $('.main_form .row .list').append('<div class="row file"></div>');
            rowFile.append('<div class="input-field col s2"><input name="filename' + i + '" type="text" value="file_' + i + '.jpg"/><label for="filename' + i + '">File name</label></div>');
            rowFile.append('<div class="input-field col s10"><input name="fileurl' + i + '" type="text" value="' + files[i] + '"/> <label for="fileurl' + i + '">URL</label></div>');
        }

        $('.main_form input').on('input paste', function () {
            update();
        });

        update();
    }

    function getJsonForm() {
        const form = $('.main_form').serializeArray();
        const result = {
            archiveName: '',
            files: []
        };

        for (let i = 0; i < form.length; i++) {
            const n = form[i].name;
            const v = form[i].value;
            if (n === 'archivename') {
                result.archiveName = v;
            } else if (n.indexOf('filename') >= 0) {
                if (result.files[parseInt(n.slice(-1))]) {
                    result.files[parseInt(n.slice(-1))].name = v;
                } else {
                    result.files[parseInt(n.slice(-1))] = ({'name': v});
                }
            } else if (n.indexOf('fileurl') >= 0) {
                if (result.files[parseInt(n.slice(-1))]) {
                    result.files[parseInt(n.slice(-1))].url = v;
                } else {
                    result.files[parseInt(n.slice(-1))] = ({'url': v});
                }
            }
        }

        return result;
    }

    function update() {
        jsonForm = getJsonForm();
    }

    $('.submit').on('click', function () {
        const xhr = new XMLHttpRequest();
        xhr.open("POST", "/archive/?_=" + new Date().getTime(), true);
        xhr.setRequestHeader("Content-type", "application/json");
        xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                const blob = new Blob([xhr.response], {type: "octet/stream"});
                const fileName = jsonForm.archiveName.trim() !== '' ? jsonForm.archiveName + '.zip' : "archive.zip";
                const URL = window.URL || window.webkitURL;
                const downloadUrl = URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = downloadUrl;
                a.download = fileName;
                document.body.appendChild(a);
                a.click();
            }
        };
        xhr.responseType = "arraybuffer";
        xhr.send(JSON.stringify(jsonForm, null, '\t'));
    });

    initForm();
});