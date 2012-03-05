function recalcula_alturas() {
  $('#region-contenido #relleno-contenido').height(0);
  var alt_options = $('#region-lateral-der').height();
  var alt_body = $('#region-contenido').height();
  if (alt_options > alt_body) {
    if ( $('#region-contenido #relleno-contenido').length > 0 ) {
      $('#region-contenido #relleno-contenido').height(alt_options - alt_body + 2); //.css('min-height', alt_options - alt_body + 2);
    } else {
      if ( $('#region-contenido #contacto').length > 0 ) {
        $('.bloque:last').append($('<div id="relleno-contenido" />').height(alt_options - alt_body + 2));
      } else {
        $('.bloque:last').append($('<div id="relleno-contenido" />').height(alt_options - alt_body + 2));
        $('#region-contenido').css('border','none');
      }
    }
  } else {
    $('#region-lateral-der').css('min-height', alt_body - 2);
  }
}


$(document).ready(function(){
  //Si estamos realmente en la front page...
  if ( $('#region-contenido #region-contenido-der').length > 0 ) {
    $('#region-contenido').css('border','none');
    //se eliminan las clases bolque y bloque-doble 
    $('.bloque').removeClass('bloque');
    $('.bloque-doble').removeClass('bloque-doble');
    
    //se activa el roller de los recortes de prensa
    $('#revista-prensa-listado').wrap($('<div class="fondo-blanco"></div>')).vTicker({
      speed: 1000,
      pause: 3000,
      showItems: 1,
      animation: 'fade',
      mousePause: true
    });
  }
  
  //Si encontramos contenido migrado se reestructura  
  $('#region-contenido #pie-info-modificacion').attr('id', 'contacto');
  $('#contacto').prepend($('#informacio-proporcionada')); 
  $('#informacio-proporcionada').wrapInner('<h2></h2>');
  $('#informacio-proporcionada').append($('#informacio-proporcionada a'));
	$('#informacio-proporcionada a').wrapInner('<h3></h3>');
  $('#contacto').prepend($('.titolblau').parent().parent().parent());
  $('#region-contenido').append( $('#contacto') );
  $('.titolblau').wrap('<h2></h2>');
  
  //$('hr').remove();
  $('img[src=http://www.uji.es/local/img/sauji/icono/punt-r.jpg]').replaceWith('<img src="/xpf/fichero/IMATGES_GENERIQUES/211415/ARXIU/guion.gif"');
  $('img[src=http://www.uji.es/local/img/sic/pixela.gif]').remove();
  $('img[src=/xpf/fichero/IMATGES_GENERIQUES/698238/ARXIU/separador.gif]').remove();
  
  //Remove font tags
  /*
  $('font').append(function(index,html){
    $(this).remove();
    return html;
  });
  */
    
  //Comportamiento de ON/OFF en los logos del pie
  var old_src = '';
  $('#pie-marcas img').hover(
    function () {
      old_src = $(this).attr('src');
      str_pos = old_src.search(".png");
      new_src = old_src.substring(0, str_pos) + "-on" + old_src.substring(str_pos);
      $(this).attr('src', new_src);
    },
    function () {
      $(this).attr('src', old_src);
    }
  );
});

$(window).load(function(){
  //Si estamos realmente en la front page...
  if ( $('#region-contenido #region-contenido-der').length > 0 ) {
    //Se iguala la altura de las regiones interiores del fron-page del portal
    var alt_der = $('#region-contenido-der').height();
    var alt_izq = $('#region-contenido-izq').height();
    if (alt_izq > alt_der) {
      $('#region-contenido #region-contenido-der').height(alt_izq);
    } else {
      $('#region-contenido #region-contenido-izq').height(alt_der);
    }
  }

  //Se iguala la altura del menu lateral
  recalcula_alturas();
});