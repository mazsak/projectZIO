function getSubtasks() {
    var inputs = document.getElementsByTagName("input");
    var id_list = [];
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].type === "checkbox" && inputs[i].checked === true
            && inputs[i].name !== "skip_task" && inputs[i].name !== "previous_task") {
            id_list.push(inputs[i].id)
        }
    }
    console.log(id_list);
    return id_list;
}

function getTasks() {
    var inputs = document.getElementsByTagName("input");
    var id_list = [];
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].type === "checkbox" && inputs[i].checked === true) {
            id_list.push(inputs[i].id)
        }
    }
    console.log(id_list);
    return id_list;
}

function validateTaskForm() {
    if (getSubtasks().length === 0){
        alert("Select at list one subtask");
        return false;
    }
    return true;
}

function validateWorkflowForm() {
    if (getSubtasks().length === 0){
        alert("Select at list one task");
        return false;
    }
    return true;
}