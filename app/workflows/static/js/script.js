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
    for (var i = 0; i < selectedElements.length; i++) {
        getStatus(idWorkflow, selectedElements[i]);
    }
}

function selectAllAction() {
    var inputs = document.getElementsByTagName("input");
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].type === "checkbox" && inputs[i].name === "user_checkbox") {
            inputs[i].checked = true;
        }
    }
}

function pauseSelectedAction() {
    var selectedElements = getElements()
    //TODO: trzeba endpointy zrobic
}

function stopSelectedAction() {
    var selectedElements = getElements()
    //TODO: trzeba endpointy zrobic
}

function deleteSelectedAction(idWorkflow) {
    var selectedElements = getElements()
    deleteUser(idWorkflow, selectedElements)
}

function updateWrokflow(id, type, update) {
    updateSkipPrevious(id, type, update);
}

function getStatus(id, idUser) {
    getStatus(id, idUser)
}

const deleteUser = async (idWorkflow, ids) => {
    try {
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
        axios.defaults.xsrfCookieName = "csrftoken";
        const res = await axios({
            method: 'delete',
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
        axios.defaults.xsrfCookieName = "csrftoken";
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
        axios.defaults.xsrfCookieName = "csrftoken";
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
        axios.defaults.xsrfCookieName = "csrftoken";
        const res = await axios({
            method: 'post',
            url: URL_BASIC + '/workflows/status',
            data: {
                id: id,
                idUser: idUser
            }
        });
        let ele = document.getElementById('status_' + idUser);
        ele.innerHTML = res.data;
        setTimeout(function () {
            getStatus(id, idUser);
        }, 1000);
        console.log('Update Todo ID: ', id, ' idUser: ', idUser);
        console.log(res.data);

        return res.data;
    } catch (e) {
        console.error(e);
    }
}

