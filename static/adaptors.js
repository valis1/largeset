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