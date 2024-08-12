
async function showNames() {
    const selectList = document.getElementById("selectList");
    const selectedGroup = selectList.value;
    const namesContainer = document.getElementById("namesContainer");
    namesContainer.innerHTML = ""; // Clear previous content
    const response = await fetch('/names');
    const data = await response.json();
    const names = data.reduce((acc, curr) => {
    if (!acc[curr.group]) {
        acc[curr.group] = [];
    }
    acc[curr.group].push([curr.name, curr.attended]);
    return acc;
}, {});
    console.log(names)
    let selectedNames;
    if (selectedGroup === "all") {
        selectedNames = Object.values(names).flat(); // Все имена из всех групп
    } else {
        selectedNames = names[selectedGroup]; // Имена из выбранной группы
    }

    selectedNames.forEach((arr,count) => {
        var name = arr[0]
        var attended = arr[1]
        const nameContainer = document.createElement("div");
        nameContainer.classList.add("name-container");
//        ${+count+1}.
        nameContainer.textContent = ` ${+count+1}. ${name}`;
        nameContainer.setAttribute('origin_name', name)

        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.name = "attendance";
        checkbox.value = name;

        nameContainer.appendChild(checkbox);
        namesContainer.appendChild(nameContainer);
        if(attended){
            nameContainer.classList.add("checked");
            checkbox.checked = true;
        }
        // Добавляем обработчик события для изменения цвета фона контейнера при клике
        nameContainer.addEventListener("click", function() {
            if (checkbox.checked) {
                nameContainer.classList.remove("checked");
                nameContainer.classList.remove("now");

                checkbox.checked = false;
            } else {
                
                nameContainer.classList.add("checked");
                nameContainer.classList.add("now");
                checkbox.checked = true;
            }
        });
    });
}

async function submitAttendance(event) {
    event.preventDefault(); // Предотвращаем стандартное поведение формы
//    alert()
    const selectedNames = Array.from(document.querySelectorAll('.name-container'))
    .map(container => {
        const name = container.getAttribute('origin_name').trim();
        const checked = container.classList.contains('checked');
        return { name, checked };
    });

    const response = await fetch('/attendance', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ names: selectedNames }) // Отправляем имена в виде объекта с ключом "names"
    });
    console.log(selectedNames)
    const data = await response.json();
    alert(data.message);
     location.reload()
}

showNames()
var copyVar=''
const copy = () =>{
document.querySelectorAll('.name-container:not(.checked)').forEach(each =>{
    copyVar += (each.getAttribute('origin_name') +'\n')
})
navigator.clipboard.writeText(copyVar).then(function() {
  console.log('Текст успешно скопирован в буфер обмена');
}, function(err) {
  console.error('Произошла ошибка при копировании текста: ', err);
});}