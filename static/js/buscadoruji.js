       function eliminaaccents(entrada) {
          var AUX = "";
          var __r = { 225:'a',224:'a',193:'A',192:'A',
                      233:'e',232:'e',201:'E',200:'E',
                      237:'i',236:'i',205:'I',204:'I',
                      243:'o',242:'o',211:'O',210:'O',
                      250:'u',249:'u',218:'U',217:'U'};

          var TEMPORAL;

          //Recorrer l'string i elimiar els accents
          for (i=0;i<entrada.length;i++) {
               TEMPORAL=__r[entrada.charAt(i).charCodeAt(0)];
               if (TEMPORAL=="undefined"  || TEMPORAL==undefined) {
                   TEMPORAL=entrada.charAt(i);
               }
               AUX += TEMPORAL;
          }
          return AUX;
       }

