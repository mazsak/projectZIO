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

function executeSelectedAction() {
    var selectedElements = getElements()
    //TODO: trzeba endpointy zrobic
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

const deleteUser = async (idWorkflow, ids) => {
    try {
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
        axios.defaults.xsrfCookieName = "csrftoken";
        const res = await axios({
            method: 'delete',
            url: 'http://127.0.0.1:8000/czarymary/hokus/pokus/json/mendoza/zrob/endpointa/' + idWorkflow,
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