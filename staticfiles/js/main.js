function carregarCampanhas() {
    fetch("../dados/campanhas.json")
        .then((res) => {
        return res.json();
        })
        .then((conteudo_json) => {
        // Aqui você pode percorrer os dados e adicionar os elementos
        for (let i = 0; i < conteudo_json.length; i++) {
            adicionarElementoCampanha(conteudo_json[i]);
            editarCampanhas(conteudo_json[i])
        }
        })
        .catch((erro) => {
        console.error("Erro ao carregar as campanhas:", erro);
        });
    }
    /*NÃO SABERMOS SE FUNCIONA */
    function editarCampanhas(campanha){
        fetch('campanhas.json')
            .then(response => {
                if (!response.ok) {
                throw new Error('Erro ao obter o arquivo JSON');
                }
                return response.text();  // Obtém o conteúdo do arquivo como string
            })
            .then(jsonString => {
                const jsonData = JSON.parse(jsonString); // Converte para objeto JavaScript
                console.log(jsonData.nome); // Acessa um valor
                jsonData.nome = "Eureca";      // Modifica um valor
                const jsonAtualizado = JSON.stringify(jsonData); // Converte de volta para string JSON
                console.log(jsonAtualizado); // Mostra o JSON atualizado
                //  Aqui você poderia salvar o jsonAtualizado em um arquivo ou enviar para um servidor
            })
            .catch(error => {
                console.error('Erro:', error);
            });
    }
    
    
    function adicionarElementoCampanha(campanha) {      
        const container = document.getElementById("campanhas");
        // Criar um novo elemento para a campanha
        const sectionCampanha = document.createElement("section");
        sectionCampanha.setAttribute("id", campanha.nome);            
        sectionCampanha.classList.add("campanha", "item2");
    
        // Adicionar conteúdo à campanha
        sectionCampanha.innerHTML = `<a>
            <h3>${campanha.nome}</h3>
            <p>${campanha.descricao}</p></a>
            <button>Acessar</button>
        `;
        
        // Adicionar o novo elemento ao container
        container.appendChild(sectionCampanha);
        
        
        }