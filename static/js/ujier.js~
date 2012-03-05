$(document).ready(function(){
  //Se limpia y ajusta el marcado del ujier antiguo
  $('*[width=550]').attr('width', '690');
  $('*[width=245]').attr('width', '320');
  
  $('.grupoRojo').siblings().remove();
  $('.noticiacuerpo').parent().parent().remove();
  $('.noticiatitular').parent().next().remove();
  $('.noticiatitular').wrapInner('<h2 class="bocadillo-rojo"></h2>');
  $('.bocadillo-rojo').append('<span class="flecha-bocadillo"></span>');
  $('.noticiatitular').append('<div id="botones-colapsar-ujier"><span class="boton-cerrar">cerrar todos</span> | <span class="boton-abrir">abrir todos</span> | <span class="boton-cambiar">cambiar</span></div>');
  
  $('.list b').next().remove();
  $('.list b').wrap('<div class="cap-nivel3"></div>');
  $('.list li').removeAttr('style');
  $('#region-contenido #contenido-ujier img').remove();
  //$('.cap-nivel3').append( '<img src="imagenes/ico_abierto_p.png" width="12" height="7" alt="menú abierto" class="ujier-arrow" />' );
  $('.cap-nivel3').append( '<img src="/img/portal2/imagenes/ico_abierto_p.png" width="12" height="7" alt="menú abierto" class="ujier-arrow" />' );  
  
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
  $('#region-contenido #contenido-ujier .cap-nivel3').click(function() {
    mychildren = $(this).next('ul');
    myarrow = $(this).find('img');
    mychildren.animate({height: 'toggle'}, 300);
    mysrc = myarrow.attr('src');
    if (mysrc.search('cerrado_p') != -1 ) {
      //myarrow.replaceWith( '<img src="imagenes/ico_abierto_p.png" width="12" height="7" alt="menú abierto" class="ujier-arrow" />' );
      myarrow.replaceWith( '<img src="/img/portal2/imagenes/ico_abierto_p.png" width="12" height="7" alt="menú abierto" class="ujier-arrow" />' );
      return false;
    } else if (mysrc.search('abierto_p') != -1 ) {
      //myarrow.replaceWith( '<img src="imagenes/ico_cerrado_p.png" width="7" height="12" alt="menú cerrado" class="ujier-arrow" />' );
      myarrow.replaceWith( '<img src="/img/portal2/imagenes/ico_cerrado_p.png" width="7" height="12" alt="menú cerrado" class="ujier-arrow" />' );
      return false;
    }
  });
  //--Colapsar cerrar todos
  $('#region-contenido #contenido-ujier #botones-colapsar-ujier .boton-cerrar').click(function() {
    mychildren = $('#region-contenido #contenido-ujier .cap-nivel3').next('ul');
    mychildren.hide(0);
    //$('#region-contenido #contenido-ujier .cap-nivel3 .ujier-arrow').replaceWith( '<img src="imagenes/ico_cerrado_p.png" width="7" height="12" alt="menú cerrado" class="ujier-arrow" />' );
    $('#region-contenido #contenido-ujier .cap-nivel3 .ujier-arrow').replaceWith( '<img src="/img/portal2/imagenes/ico_cerrado_p.png" width="7" height="12" alt="menú cerrado" class="ujier-arrow" />' );
    return false;
  });
  //--Colapsar abrir todos
  $('#region-contenido #contenido-ujier #botones-colapsar-ujier .boton-abrir').click(function() {
    mychildren = $('#region-contenido #contenido-ujier .cap-nivel3').next('ul');
    mychildren.show();
    //$('#region-contenido #contenido-ujier .cap-nivel3 .ujier-arrow').replaceWith( '<img src="imagenes/ico_abierto_p.png" width="12" height="7" alt="menú abierto" class="ujier-arrow" />' );
    $('#region-contenido #contenido-ujier .cap-nivel3 .ujier-arrow').replaceWith( '<img src="/img/portal2/imagenes/ico_abierto_p.png" width="12" height="7" alt="menú abierto" class="ujier-arrow" />' );
    return false;
  });
  //--Colapsar abrir cerrados y cerrar abiertos
  $('#region-contenido #contenido-ujier #botones-colapsar-ujier .boton-cambiar').click(function() {
    $('#region-contenido #contenido-ujier .cap-nivel3').click();
    return false;
  });
});