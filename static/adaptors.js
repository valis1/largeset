//To-do Refactor to mixins
function to_csv(json_data, header, delimiter) {
    let result_string = '';
    let data = JSON.parse(json_data);

    //Форматируем заголовок 
    if (header) {
        for (key of Object.keys(data.data[0])){
            result_string += `${key}${delimiter}`;
        }
        result_string += '\n';
    }
    for (row of data.data) {
        for (key of Object.keys(row)){
            result_string += `${row[key]}${delimiter}`;
        }
        result_string += '\n';   
    }
    const blob = new Blob([result_string], {type: 'text/csv; charset=utf-8'});
    return blob;
}

function to_json(json_data, root_element) {
    let result_object ={};
    let data = JSON.parse(json_data);
    if (root_element.length > 0) {
        result_object[root_element] = data.data;
    }
    else {
        result_object = data.data;
    }
    return new Blob([JSON.stringify(result_object)], {type: 'application/json; charset=utf-8'}); 
}

function to_dbunit(json_data, table_name){
    let res = `<?xml version='1.0' encoding='UTF-8'?>
    <dataset>\n`;
    let data = JSON.parse(json_data);
    for (row of data.data) {
        res += `<${table_name} `;
        for (key of Object.keys(row)){
            res += `${key} = "${row[key]}" `;
        }
        res += '/>\n';
    }
    res += '</dataset>';
    const blob = new Blob([res], {type: 'application/xml; charset=utf-8'});
    return blob;
}