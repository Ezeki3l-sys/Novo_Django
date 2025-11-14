  // Salva o tema padrão se não existir
  if (!localStorage.getItem("tema")) {
    localStorage.setItem("tema", "Feiticaria");
  }

  // Função para aplicar o tema pelo nome
  function aplicarTema(nomeTema) {
    switch(nomeTema) {
      case "Druida":
        aplicarTemaDruida();
        break;
      case "Feiticaria":
        aplicarTemaFeiticaria();
        break;
      case "Cavaleiro":
        aplicarTemaCavaleiro();
        break;
      case "Profundo":
        aplicarTemaProfundo();
        break;
      case "Draconico":
        aplicarTemaDraconico();
        break;
      default:
        aplicarTemaFeitiçaria(); // tema padrão
    }
  }

  // Quando a página carrega, aplica o tema salvo
  window.onload = function() {
    const temaSalvo = localStorage.getItem("tema");
    aplicarTema(temaSalvo);
  }

  function aplicarTemaDruida() {
    document.documentElement.style.setProperty('--cor-fundo', '#0a3740');
    document.documentElement.style.setProperty('--cor-texto', 'rgb(146, 232, 159)');
    document.documentElement.style.setProperty('--cor-destaque', '#4CAF50');
    localStorage.setItem("tema", "Druida");
  }

  function aplicarTemaFeiticaria() {
    document.documentElement.style.setProperty('--cor-fundo', '#2f1335');
    document.documentElement.style.setProperty('--cor-texto', '#ffffff');
    document.documentElement.style.setProperty('--cor-destaque', '#ce3762');
    localStorage.setItem("tema", "Feiticaria");
  }

  function aplicarTemaCavaleiro() {
    document.documentElement.style.setProperty('--cor-fundo', '#000000');
    document.documentElement.style.setProperty('--cor-texto', '#ffffff');
    document.documentElement.style.setProperty('--cor-destaque', '#ffb752');
    localStorage.setItem("tema", "Cavaleiro");
  }

  function aplicarTemaProfundo() {
    document.documentElement.style.setProperty('--cor-fundo', '#03223f');
    document.documentElement.style.setProperty('--cor-texto', '#e19f41');
    document.documentElement.style.setProperty('--cor-destaque', '#038bbb');
    localStorage.setItem("tema", "Profundo");
  }

  function aplicarTemaDraconico() {
    document.documentElement.style.setProperty('--cor-fundo', '#5a3546');
    document.documentElement.style.setProperty('--cor-texto', '#ffffff');
    document.documentElement.style.setProperty('--cor-destaque', '#fc6747');
    localStorage.setItem("tema", "Draconico");
  }