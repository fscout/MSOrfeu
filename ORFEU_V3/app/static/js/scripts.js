
window.onload = function() {
    formataMoeda();
  };

function formataMoeda() {
        valor = document.getElementsByClassName("valor")
        for (let v = 0; v < valor.length; v++) {
            aux = parseFloat(valor[v].innerText)
            valor[v].innerText = aux.toLocaleString('pt-br',{style: 'currency', currency: 'BRL'});
        }
}

function msg(valor) {
    switch (valor) {
        case 1:
            alert("Criado com sucesso!")
            break;
        case 2:
            alert("alterado com sucesso!")
            break;
        case 3:
            alert("Apagado com sucesso!")
            break;
        default:
            alert("Não existe!")
            break;
    }
}
 

function add_categoria()
{
var id_categ_select = document.getElementById("id_categ_select");
var id_categoria = document.getElementById("id_categoria");
// var id_categoria = document.getElementsByName("id_categoria");
// alert(id_categ_select.value)
// alert(typeof(id_categ_select.value))
// alert(id_categoria.value)
id_categoria.value = id_categ_select.value
}

function add_marca()
{
var id_marca_select = document.getElementById("id_marca_select");
var id_marca = document.getElementById("id_marca");
id_marca.value = id_marca_select.value
}

function add_medida()
{
var id_medida_select = document.getElementById("id_medida_select");
var id_medida = document.getElementById("id_medida");
id_medida.value = id_medida_select.value
}


// function converteParaMaiuscula() 
// {
// var texto = document.getElementById("descricao_prod");
// texto.value = texto.value.toUpperCase();
// }

function converteParaMaiuscula()
{
var texto = document.getElementsByClassName("convertePMaiuscula");
for (let palavra = 0; palavra < texto.length; palavra++) {
    texto[palavra].value = texto[palavra].value.toUpperCase();
}
}





function envia_dados() {
    $.ajax({
        url: '/signUpUser',
        data: $('form').serialize(),
        type: 'POST',
        success: function(response) {
            console.log(response);
        },
        error: function(error) {
            console.log(error);
        }
    });
}
// function envia_dados() {
//     $.ajax({
//         url: '/add_categoria',
//         data: $('form').serialize(),
//         type: 'POST',
//         success: function(response) {
//             console.log(response);
//             alert("Cadastrado")
//         },
//         error: function(error) {
//             console.log(error);
//         }
//     });
// }



function msg_produto_cadastrado(){
    alert("Produto já cadastrado!")
}





function add_nivel()
{
var id_nivel_select = document.getElementById("id_nivel_select");
var id_nivel_acesso_id = document.getElementById("id_nivel_acesso_id");
id_nivel_acesso_id.value = id_nivel_select.value
}