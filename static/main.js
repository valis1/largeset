
Vue.component('modal', {
    template: '#modal-template',
    props: ['items'],
        
    });

var app = new Vue({
    el: '#app',
    data: {
        filtered_items:[],
        current_editable_model: {},
        showModal:false,
        data_processed:false,
        success_request_allert: false,
        request_time: 1,
        file_type: 'text',
        delimiter: ';',
        header: true,
        main_form: {
            null_method: 'percent_optimized',
            language: 'ru',
            data_len: 10,
            fields: [
                {id:'TextField1', percent_nulls:0, null:true, sctript:'', type:'int'},
                {id:'NumericField2', percent_nulls:0, null:false, sctript:'', type:'int'},
                {id:'DatetimeField3',percent_nulls:0, null:false, sctript:'', type:'int'}
            ]
        },
        items: []
    },
    methods: {
        add_row(){
            this.main_form.fields.push({id:'new_field', percent_nulls:0, null:true, sctript:'', type:'int'});
        },
        del_row(index){
            this.main_form.fields.splice(index,1);
        },
        filter_event(text){
            if (text.length > 0) {
                this.filtered_items = this.items.filter(item => item.desc.toLowerCase().indexOf(text.toLowerCase())!=-1);
            }
            else {
                this.filtered_items= [];
            }
        },
        modal_event(model){
            this.current_editable_model = model;
            this.showModal = true;
        },
        close_allert(){
           this.success_request_allert = false;
        },
        type_select_event(value, script){
            this.current_editable_model.type = value;
            this.current_editable_model.sctript = script;
            this.showModal = false;
            this.filtered_items = [];
        },
        get_data(){
            let xhr = new XMLHttpRequest();
            this.data_processed = true;
            start_time = new Date().getTime()
            xhr.open('POST','/service/',true);
            xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
            xhr.send(JSON.stringify(this.main_form));
            xhr.onreadystatechange =() => {
                if (xhr.readyState == 4) {
                    this.data_processed = false;
                    if (xhr.status != 200) {
                        alert( xhr.status + ': ' + xhr.statusText ); 
                      } else {
                          let blob;
                          let file_type;
                          if (this.file_type == 'text') {
                              blob = to_csv(xhr.responseText, this.header, this.delimiter);
                              file_type='.csv';
                          }
                          if (blob){
                            let link = document.createElement('a');
                            link.href  = window.URL.createObjectURL(blob);
                            link.download = 'results' + file_type
                            this.request_time = new Date().getTime() - start_time
                            this.success_request_allert = true;
                            link.click();
                          }
                          else {
                              console.log('Чет не получилось нет блоба');//Нужно как-то вывести предупреждение
                          }
                      }
                }
            };
        }
    },
    created: function(){
        let xhr = new XMLHttpRequest();
        xhr.open('GET', '/fields', true)
        xhr.send()
        xhr.onreadystatechange = () => {
            if (xhr.readyState == 4) {
                if (xhr.status != 200) {
                    this.items = [{'id': 'noData', 'desc': 'No Data', 'example': 'Something got wrond', 'script': '', 'resolved_functions':[]},]
                  } else {
                this.items = JSON.parse(xhr.responseText);
        }
    }
    
}
},
    computed: {
        sorted_items: function(){
            let result = [[]];
            let this_items = this.items;
            if (this.filtered_items.length > 0) {
                this_items = this.filtered_items;
            }
            let cnt = 0;
            let res_index = 0;
            for (let item of this_items) {
                if (cnt == 4) {
                    cnt = 0;
                    result.push([]);
                    res_index++;
                }
                result[res_index].push(item);
                cnt++;
            }
            return result;
        }
    }
}
);