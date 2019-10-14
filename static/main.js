String.prototype.replaceAll = function(search, replace){
    return this.split(search).join(replace);
  }

Vue.component('modal', {
    template: '#modal-template',
    props: ['items'],
    data: function(){
        return {
            filtered_items:[]
        }
    },
    computed: {
        distributed_items: function(){
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
        },
    },
    methods: {
        filter_event(text){
            if (text.length > 0) {
                this.filtered_items = this.items.filter(item => item.desc.toLowerCase().indexOf(text.toLowerCase())!=-1);
            }
            else {
                this.filtered_items= [];
            }
        },
    }  
    });

Vue.component('scriptmodal', {
    template: '#script-modal',
    props: ['editable', 'items'],
    computed: {
        formated_text: function(){
            return this.editable.sctript.replaceAll(';', ';' + '\n').replaceAll(' ', '')
        },
        item_funcs: function(){
            for (item of this.items){
                if (item.id == this.editable.type){
                    return item.resolved_functions;
                }
            }
        }
    },
    methods: {
        close: function(){
            this.$emit('close', this.$refs.edited_text.value)
        },
        start_drag: function(e){
            e.target.style.opacity = '0.1';
            e.dataTransfer.setData("text", e.target.innerText);
            e.dataTransfer.effectAllowed = "move";
        },
        end_drag: function(e) {
            e.target.style.opacity='0.9';
        },
        dragenter: function(e){
            e.preventDefault();
            e.target.classList.toggle('border');
            e.target.classList.toggle('border-primary');
        },
        dragleave: function(e){
            e.target.classList.toggle('border');
            e.target.classList.toggle('border-primary');
        },
        on_drop: function(e){
            if (this.$refs.edited_text.value.length >0) {
            this.$refs.edited_text.value += '\n' + e.dataTransfer.getData('text') + ';'
            }
            else {
                this.$refs.edited_text.value =  e.dataTransfer.getData('text') + ';'
            }
        },
        dragover: function(e){
            e.preventDefault();
            e.dataTransfer.dropEffect = "move";
        }

    }
    
});

Vue.component("schema-modal",{
    template:"#load-modal",
    props: ['model', 'id_of_schema'],
    data: function() {
        return {
            schema_id: '',
            show_allert: false,
            allert_text: '',
            schema: false
        }
    },
    methods: {
        save_schema(){

            let xhr = new XMLHttpRequest();
            if (this.schema_id.length == 0){
                xhr.open("POST", "/schemas/",true);
                xhr.send(JSON.stringify(this.model));
                xhr.onreadystatechange =() => {
                    if(xhr.readyState ==4) {
                        if (xhr.status != 200) {
                            this.allert_text = `Schema not saved! Error!`
                        } else { 
                             let result = JSON.parse(xhr.responseText);
                             this.schema_id = result.schema_id;
                             this.allert_text = `Schema saved!`
                        }
                    
                    }
                }
            }
            else if (this.schema_id.length == 24) {
                xhr.open("PUT", `/schemas?schema_id=${this.schema_id}`,true);
                xhr.send(JSON.stringify(this.model));
                xhr.onreadystatechange =() => {
                    if(xhr.readyState ==4) {
                        if (xhr.status == 401) {
                            this.allert_text = `Schema not found`
                        }
                        else if (xhr.status != 200 ) {
                            this.allert_text = `Server Error`
                        }
                        else { 
                             let result = JSON.parse(xhr.responseText);
                             this.allert_text = `Schema updated!`
                             this.show_allert = true;
                        }
                    
                    }
                }

            }
            else {
                this.allert_text = 'Schema ID must be 24 symbols length or empty'
            }
            this.show_allert = true;
        },
        get_schema(){
            let xhr = new XMLHttpRequest();
            if (this.schema_id.length == 24) {
            xhr.open("GET", `/schemas?schema_id=${this.schema_id}`,true);
            xhr.send();
            xhr.onreadystatechange =() => {
                if(xhr.readyState ==4) {
                    if (xhr.status == 401) {
                        this.allert_text = `Schema not found`;
                      } 
                    else if (xhr.status != 200) {
                        this.allert_text = `Server Error`;
                    }
                    else { 
                         let result = JSON.parse(xhr.responseText);
                         this.schema = result;
                         this.allert_text = `Schema Loaded!`
                      }
                      this.show_allert = true;
                    
                }
            }
            }
            else {
                this.allert_text ='Schema ID must be 24 symbols length';
                this.show_allert = true;
            }
        },
        copy_to_clipboard() {
            let input = this.$refs.schema_id_input;
            input.select();
            document.execCommand('copy');
            this.allert_text = "Success copy to clipboard"
            this.show_allert = true;
        }
    },
    created: function(){
        if (this.id_of_schema!= '') {
            this.schema_id = this.id_of_schema;
        }
    }
})

var app = new Vue({
    el: '#app',
    data: {
        filtered_items:[],
        current_editable_model: {},
        showModal:false,
        showScriptModal:false,
        showSchemaDialog: false,
        data_processed:false,
        success_request_allert: false,
        allert_text:'',
        file_type: 'text',
        delimiter: ';',
        json_root: 'data',
        header: true,
        encoding: 'utf-8',
        table_name:'MY_TABLE',
        schema_id: '',
        main_form: {
            language: 'ru',
            data_len: 10,
            fields: [
                {id:'Company_Name',percent_nulls:0, null:false, sctript:'', type:'company'},
                {id:'Date_Start', percent_nulls:0, null:false, sctript:'', type:'datetime'},
                {id:'Employees', percent_nulls:0, null:true, sctript:'', type:'int'},

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
        modal_event(model){
            this.current_editable_model = model;
            this.showModal = true;
        },
        scrypt_modal_event(model){
            this.current_editable_model = model;
            this.showScriptModal = true;
        },
        close_scrypt_modal(text){
            this.current_editable_model.sctript = text.replaceAll('\n','');
            this.showScriptModal=false;
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
        close_dialog_and_get_model(model, id){
            if (model) {
            if (id != this.schema_id) {
                this.main_form = model;
                this.schema_id = id;
                this.allert_text = "Schema loaded!";
                this.success_request_allert = true;
            }
        }
        this.showSchemaDialog =false;
        this.schema_id = id;
        },
        get_data(){
            let xhr = new XMLHttpRequest();
            this.data_processed = true;
            let start_time = new Date().getTime();
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
                          else if (this.file_type == 'json'){
                              blob = to_json(xhr.responseText, this.json_root);
                              file_type = '.json';
                          }
                          else if (this.file_type == 'dbunit'){
                              blob = to_dbunit(xhr.responseText, this.table_name);
                              file_type = '.xml'
                             

                          }
                          if (blob){
                            let link = document.createElement('a');
                            link.href  = window.URL.createObjectURL(blob);
                            link.download = 'results' + file_type
                            let request_time = new Date().getTime() - start_time
                            this.allert_text = `Success! Data generated at time: ${request_time} ms`
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
});