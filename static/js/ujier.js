$(document).ready(function(){
  //$('.noticiatitular').wrapInner('<h2 class="bocadillo-rojo"></h2>');
  $('.bocadillo-rojo').append('<span class="flecha-bocadillo"></span>');
  
  $('.list span.list').next().remove();
  $('.list span.list').wrap('<div class="cap-nivel3"></div>');
  $('.list li').removeAttr('style');
  
  $('.list2 span.list2').next().remove();
  $('.list2 span.list2').wrap('<div class="cap-nivel4"></div>');
  $('.list li').removeAttr('style');
  
  $('.cap-nivel3').append( '<span class="desplegable_niv3"><img class="desplegable_niv3" src="/media/img/ico_abierto_p.png" width="12" height="7" alt="men� abierto"/></span>' );  
  $('.cap-nivel4').append( '<span class="desplegable_niv4"><img class="desplegable_niv4" src="/media/img/ico_abierto_p.png" width="12" height="7" alt="men� abierto"/></span>' );
  
  //Se iguala la altura del menu lateral
  var alt_options = $('#region-lateral-der').height();
  var alt_body = $('#region-contenido').height();
  if (alt_options > alt_body) {
    $('#region-contenido > div.bloque').height(alt_options);
    $('#region-lateral-der').height(alt_options + 30);
  } else {
    $('#region-lateral-der').height(alt_body + 30);
    $('#region-contenido > div.bloque').height(alt_body);
  }
  
  //Comportamientos de los colapsables del ujier
  
  colapsable_niv3 = function() {
	  	if (this.nodeName=="B"){
	  		elem = $(this.parentElement.parentElement);
	  	}
	  	else {
	  		elem = $(this.parentElement);
	  	}
	    mychildren = elem.next('ul');
	    myarrow = elem.find('img.desplegable_niv3');
	    mychildren.animate({height: 'toggle'}, 300);
	    mysrc = myarrow.attr('src');
	    if (mysrc.search('cerrado_p') != -1 ) {
	      myarrow.replaceWith( '<img class="desplegable_niv3" src="/media/img/ico_abierto_p.png" width="12" height="7" alt="men� abierto"/>' );
	      return false;
	    } else if (mysrc.search('abierto_p') != -1 ) {
	      myarrow.replaceWith( '<img class="desplegable_niv3" src="/media/img/ico_cerrado_p.png" width="7" height="12" alt="men� cerrado" />' );      return false;
	    }
	  };
  
  $('#region-contenido #contenido-ujier .cap-nivel3 span.desplegable_niv3').click(colapsable_niv3);
  $('#region-contenido #contenido-ujier .cap-nivel3 span.list b').click(colapsable_niv3);
  
  colapsable_niv4 = function() {
	  	if (this.nodeName=="B"){
	  		elem = $(this.parentElement.parentElement);
	  	}
	  	else {
	  		elem = $(this.parentElement);
	  	}
	    mychildren = elem.next('ul');
	    myarrow = elem.find('img.desplegable_niv4');
	    mychildren.animate({height: 'toggle'}, 300);
	    mysrc = myarrow.attr('src');
	    if (mysrc.search('cerrado_p') != -1 ) {
	      myarrow.replaceWith( '<img class="desplegable_niv4" src="/media/img/ico_abierto_p.png" width="12" height="7" alt="men� abierto" />' );
	      return false;
	    } else if (mysrc.search('abierto_p') != -1 ) {
	      myarrow.replaceWith( '<img class="desplegable_niv4" src="/media/img/ico_cerrado_p.png" width="7" height="12" alt="men� cerrado" />' );      return false;
	    }
	  };
  
  
  $('#region-contenido #contenido-ujier .cap-nivel4 span.desplegable_niv4').click(colapsable_niv4);
  $('#region-contenido #contenido-ujier .cap-nivel4 span.list2 b').click(colapsable_niv4);
  
  //--Colapsar cerrar todos
  $('#region-contenido #contenido-ujier #botones-colapsar-ujier .boton-cerrar').click(function() {
    mychildren = $('#region-contenido #contenido-ujier .cap-nivel3').next('ul');
    mychildren.hide(0);
    $('#region-contenido #contenido-ujier .cap-nivel3 img.desplegable_niv3').replaceWith( '<img class="desplegable_niv3" src="/media/img/ico_cerrado_p.png" width="7" height="12" alt="men� cerrado"/>' );
    mychildren = $('#region-contenido #contenido-ujier .cap-nivel4').next('ul');
    mychildren.hide(0);
    $('#region-contenido #contenido-ujier .cap-nivel4 img.desplegable_niv4').replaceWith( '<img class="desplegable_niv4" src="/media/img/ico_cerrado_p.png" width="7" height="12" alt="men� cerrado" class="ujier-arrow" />' );
    return false;
  });
  //--Colapsar abrir todos
  $('#region-contenido #contenido-ujier #botones-colapsar-ujier .boton-abrir').click(function() {
    mychildren = $('#region-contenido #contenido-ujier .cap-nivel3').next('ul');
    mychildren.show();
    $('#region-contenido #contenido-ujier .cap-nivel3 img.desplegable_niv3').replaceWith( '<img class="desplegable_niv3" src="/media/img/ico_abierto_p.png" width="12" height="7" alt="men� abierto" class="ujier-arrow" />' );
    mychildren = $('#region-contenido #contenido-ujier .cap-nivel4').next('ul');
    mychildren.show();
    $('#region-contenido #contenido-ujier .cap-nivel4 img.desplegable_niv4').replaceWith( '<img class="desplegable_niv4" src="/media/img/ico_abierto_p.png" width="12" height="7" alt="men� abierto" class="ujier-arrow" />' );
    return false;
  });
  //--Colapsar abrir cerrados y cerrar abiertos
  $('#region-contenido #contenido-ujier #botones-colapsar-ujier .boton-cambiar').click(function() {
    $('#region-contenido #contenido-ujier .cap-nivel3 span.desplegable_niv3').click();
    $('#region-contenido #contenido-ujier .cap-nivel4 span.desplegable_niv4').click();
    return false;
  });
});
