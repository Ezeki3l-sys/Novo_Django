function carregarCampanhas() {
    fetch("../dados/campanhas.json")
        .then((res) => {
        return res.json();
        })
        .then((conteudo_json) => {
        // Aqui você pode percorrer os dados e adicionar os elementos
            localStorage.setItem("campanhas", conteudo_json)
        })
        .catch((erro) => {
        console.error("Erro ao carregar as campanhas:", erro);
        });
    }