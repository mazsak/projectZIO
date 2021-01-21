var URL_BASIC = "http://127.0.0.1:8080";

function getElements() {
    var inputs = document.getElementsByTagName("input");
    var id_list = [];
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].type === "checkbox" && inputs[i].name === "user_checkbox" && inputs[i].checked === true) {
            id_list.push(inputs[i].id)
        }
    }
    console.log(id_list);
    return id_list;
}

async function executeSelectedAction(idWorkflow) {
    var selectedElements = getElements();
    executeWorkflow(idWorkflow, selectedElements);
    document.location.href = '/workflows/' + idWorkflow;

}

function selectAllAction() {
    var all = document.getElementsByName("select_all")[0];
    var inputs = document.getElementsByTagName("input");
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].type === "checkbox" && inputs[i].name === "user_checkbox") {
            inputs[i].checked = all.checked;
        }
    }
}

function pauseSelectedAction(idWorkflow) {
    var selectedElements = getElements()
    //TODO: trzeba endpointy zrobic
}

function stopSelectedAction(idWorkflow) {
    var selectedElements = getElements();
    stopWorkflow(idWorkflow, selectedElements);
}

function updateWrokflow(id, type, update) {
    updateSkipPrevious(id, type, update);
}

function getStatus(id, idUser) {
    getStatus(id, idUser);
}

const stopWorkflow = async (idWorkflow, ids) => {
    try {
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
        axios.defaults.xsrfCookieName = 'csrftoken';
        const res = await axios({
            method: 'post',
            url: URL_BASIC + '/czarymary/hokus/pokus/json/mendoza/zrob/endpointa/' + idWorkflow,
            data: {
                ids: ids
            }
        });
        console.log(`Deleted Todo ID: `, ids);
        console.log(`Deleted Todo ID: `, idWorkflow);
        return res.data;
    } catch (e) {
        console.error(e);
    }
};

const executeWorkflow = async (idWorkflow, ids) => {
    try {
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
        axios.defaults.xsrfCookieName = 'csrftoken';
        const res = await axios({
            method: 'post',
            url: URL_BASIC + '/workflows/start/' + idWorkflow,
            data: {
                ids: ids
            }
        });
        console.log('Started Todo ID: ', ids);
        console.log('Started Todo ID: ', idWorkflow);
        console.log(res.data);

        return res.data;
    } catch (e) {
        console.error(e);
    }
};

const updateSkipPrevious = async (id, type, update) => {
    try {
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
        axios.defaults.xsrfCookieName = 'csrftoken';
        const res = await axios({
            method: 'post',
            url: URL_BASIC + '/workflows/update',
            data: {
                id: id,
                type: type,
                update: update
            }
        });
        console.log('Update Todo ID: ', id, ' type: ', type, ' update: ', update);
        console.log(res.data);

        return res.data;
    } catch (e) {
        console.error(e);
    }
};

async function getStatus(id, idUser) {
    try {
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
        axios.defaults.xsrfCookieName = 'csrftoken';
        const res = await axios({
            method: 'post',
            url: URL_BASIC + '/workflows/status',
            data: {
                id: id,
                idUser: idUser
            }
        });
        var counter = 0;
        var data = JSON.parse(res.data.replaceAll("'", "\""));
        for (var i = 0; i < data.length; i++) {
            let ele = document.getElementById('status_' + data[i]['id'] + '_' + idUser);
            if (data[i]['action'] === 'queue') {
                ele.className = "glyphicon glyphicon-info-sign";
                ele.style.color = 'blue';
            } else if (data[i]['action'] === 'finished') {
                ele.className = "glyphicon glyphicon-ok-sign";
                ele.style.color = 'green';
                counter++;
            } else if (data[i]['action'] === 'started') {
                ele.className = "glyphicon glyphicon-play";
                ele.style.color = 'green';
            } else if (data[i]['action'] === 'skip') {
                ele.className = "glyphicon glyphicon-minus-sign";
                ele.style.color = 'orange';
                counter++;
            }

        }

        if (data[0]["try"] !== null) {
            document.getElementById('button_log_' + idUser).hidden = true;
            document.getElementById('info_log_' + idUser).hidden = false;
        }

        if (counter !== data.length) {
            document.getElementById('button_log_' + idUser).hidden = true;
            document.getElementById('info_log_' + idUser).hidden = false;
            setTimeout(function () {
                getStatus(id, idUser);
            }, 2000);
        } else {
            document.getElementById('button_log_' + idUser).hidden = false;
            document.getElementById('info_log_' + idUser).hidden = true;
        }

        return res.data;
    } catch (e) {
        // console.error(e);

        document.getElementById('button_log_' + idUser).hidden = true;
        document.getElementById('info_log_' + idUser).hidden = false;
        setTimeout(function () {
            getStatus(id, idUser);
        }, 2000);
    }
}

