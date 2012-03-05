function autocompletadoAction(){
	nuevaAccion = "Realitza acció";
	originalAccion = "Omplir a partir del correu"
	button = document.getElementById('button_auto');
	textarea = document.getElementById('textarea_auto');
	if ( button.value != nuevaAccion ){
		textarea.style.display= "block";
		button = document.getElementById('button_auto');
		button.value=nuevaAccion;
	}
	else {
		texto = textarea.value;
		texto = texto.replace(/\r/g, '');
		lineas = texto.split(/\n/);
		fin = false;
		for ( var i = 0; i < lineas.length && !fin; i++) {
			fin = asignaValorAuto(lineas[i]);
		}
		otrosdatos= document.getElementById('id_proyecto-otrosDatos');
		otrosdatos.value = texto;
		button.value = originalAccion;
		textarea.value ="";
		textarea.style.display= "none";
	}
}

var campos = {
		'Alumne': 'id_alumno-nombre',
		'Mail':   'id_alumno-usuarioUJI',
		
		'Entitat': 'id_proyecto-empresa',
		'Supervisor': 'id_proyecto-supervisor',
		'Telefon': 'id_proyecto-telefono',
		'Data inici': 'id_proyecto-inicio'
}


function asignaValorAuto(linea){
	linea = linea.split(':');
	fin = (linea[0]=="Mail") ? true : false;
	if (campos[linea[0]]){
		if (linea.length > 1){
			linea[1] = linea[1].substring(1,linea[1].length);
			campo = document.getElementById(campos[linea[0]]);
			campo.value = limpiaCampo(linea[1], linea[0]);
		}
	}
	
	return fin;
}

function limpiaCampo(valor, campo){
	if (campo == "Data inici")
		if ( valor == "Indistint")
			return "";
	if (campo == "Mail") 
		return valor.split('@')[0];
	if (campo == "Supervisor"){
		return valor.split('(')[0]
		
	}
	return valor;
}