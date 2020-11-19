function getElements() {
    var inputs = document.getElementsByTagName("input");
    var id_list = [];
    for(var i = 0; i < inputs.length; i++) {
        if(inputs[i].type === "checkbox" && inputs[i].name === "user_checkbox" && inputs[i].checked === true) {
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
    for(var i = 0; i < inputs.length; i++) {
        if(inputs[i].type === "checkbox" && inputs[i].name === "user_checkbox") {
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

function deleteSelectedAction() {
    var selectedElements = getElements()
    deleteUser(selectedElements)
}

const deleteUser = async id => {
  try {
    const res = await axios.delete(`http://127.0.0.1:8000/czarymary/hokus/pokus/json/mendoza/zrob/endpointa/${id}`);
    console.log(`Deleted Todo ID: `, id);
    return res.data;
  } catch (e) {
    console.error(e);
  }
};