$(document).ready(function() {
    $('#toggleButton').on('click', function() {
        var display = $('.barralateralbg').css('display');
        
        if (display === 'block') {
            $('.barralateral').animate({ left: '-370px' }, 300, function() {
                $(this).css('display', 'none');
            });
            $('.barralateralbg').fadeOut(1000);
        } else {
            $('.barralateralbg').fadeIn(1000);
            $('.barralateral').css('display', 'block')
                .animate({ left: '0px' }, 300);
        }
    });

    $('.barralateralbg').on('click', function() {
        var display = $('.barralateralbg').css('display');

        $('.barralateral').animate({ left: '-370px' }, 300, function() {
            $(this).css('display', 'none');
        });
        $('.barralateralbg').fadeOut(1000);
    });

    $('#alterar').on('click', function() {
		$('#altse').css('display', 'none');
		$('#opcoes').css('display', 'block');
    });

    $('#cancelar').on('click', function() {
		$('#altse').css('display', 'block');
		$('#opcoes').css('display', 'none');
    });

    function vertam() {
        var largura = $(window).width();
        var altura = $(window).height();

        if (largura > altura) {
            if (largura > 1366) {
                $(':root').css('--box', '25vw');
                $(':root').css('--input', '20vw');
                $(':root').css('--padding', '5vh 2.5vw 5vh 2.5vw');
            } else {
                $(':root').css('--box', '40vw');
                $(':root').css('--input', '30vw');
                $(':root').css('--padding', '5vh 2vw 5vh 2vw');
            }
        } else {
            $(':root').css('--box', '40vw');
            $(':root').css('--input', '30vw');
        }
    }

    $(window).on('resize', vertam);
    vertam();
});

function excluir() {
	if (confirm('Deseja realmente excluir seu perfil?')) {
		alert('Seu perfil será excluido!');
		location.href='/excluir';
	} else {
		alert('Exclusão cancelada!');
	}
}

function logoff() {
	if (confirm('Você deseja sair do seu perfil?')) {
		location.href='/logout';
	}
}

document.addEventListener('DOMContentLoaded', () => {
	const tel = document.getElementById('tel')

	tel.addEventListener('keypress', (e) => mascaraTelefone(e.target.value))
	tel.addEventListener('change', (e) => mascaraTelefone(e.target.value))

	const mascaraTelefone = (valor) => {
		valor = valor.replace(/\D/g, "")
		valor = valor.replace(/^(\d{2})(\d)/g, "($1) $2")
		valor = valor.replace(/(\d)(\d{4})$/, "$1-$2")
		tel.value = valor
	}
});

document.addEventListener('DOMContentLoaded', () => {
    const cpf = document.getElementById('doc');

    const mascaraCPF = (valor) => {
        valor = valor.replace(/\D/g, "");
        valor = valor.replace(/(\d{3})(\d)/, "$1.$2");
        valor = valor.replace(/(\d{3})(\d)/, "$1.$2");
        valor = valor.replace(/(\d{3})(\d{1,2})$/, "$1-$2");
        cpf.value = valor;
    }

    cpf.addEventListener('keypress', (e) => mascaraCPF(e.target.value));
    cpf.addEventListener('change', (e) => mascaraCPF(e.target.value));
});

var emailAtual = "";

function editaremail() {
    var emailInput = document.getElementById('email');
    var emailLink = document.getElementById('editaemail');

    if (emailInput.readOnly) {
        emailAtual = emailInput.value;
        emailInput.value = "";
        emailLink.innerText = 'Salvar';
        emailInput.readOnly = false;
        emailInput.focus();
    } else {
        if (emailInput.value.trim() === "") {
            emailInput.value = emailAtual;
            alert("O email não pode ficar vazio!");
        } else {
            emailLink.innerText = 'Editar';
            emailInput.readOnly = true;
            document.getElementById('edteml').submit();
        }
    }
}

var telAtual = "";

function editartel() {
    var telInput = document.getElementById('tel');
    var telLink = document.getElementById('editatel');

    if (telInput.readOnly) {
        telAtual = telInput.value;
        telInput.value = "";
        telLink.innerText = 'Salvar';
        telInput.readOnly = false;
        telInput.focus();
    } else {
        if (telInput.value.trim() === "") {
            telInput.value = telAtual;
            alert("O telefone não pode ficar vazio!");
        } else {
            telLink.innerText = 'Editar';
            telInput.readOnly = true;
            document.getElementById('edttel').submit();
        }
    }
}

function valida() {
    var senhaAnt = document.getElementById('senhaant').value;
    var senhaNov = document.getElementById('senhanov').value;
    var senhaConf = document.getElementById('senhaconf').value;
    var senhaConfInput = document.getElementById('senhaconf');

    if (senhaNov !== senhaConf) {
        senhaConfInput.classList.add('error');
        alert('As senhas não coincidem.');
    } else {
        senhaConfInput.classList.remove('error');

        if(senhaAnt != "" && senhaAnt != null) {
            document.getElementById('pwdedt').submit();
        }else{
            alert("Preencha a senha atual!");
        }
    }
}