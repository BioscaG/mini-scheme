; Función para filtrar elementos de una lista según un predicado
(define (filter predicat llista)
  (if (null? llista)
      '()
      (if (predicat (car llista))
          (cons (car llista) (filter predicat (cdr llista)))
          (filter predicat (cdr llista)))))

; Predicados para filtrar
(define (parell? x)
  (= (mod x 2) 0))

(define (positiu? x)
  (> x 0))

(define (multiples-de-tres? x)
  (= (mod x 3) 0))

; Función principal
(define (main)
  ; Lista predefinida
  (define llista '(10 -3 4 0 9 -6 15 2 8))

  ; Mostrar la lista original
  (display "Llista original: ")
  (display llista)
  (newline)

  ; Filtrar números pares
  (display "Nombres parells: ")
  (display (filter parell? llista))
  (newline)

  ; Filtrar números positivos
  (display "Nombres positius: ")
  (display (filter positiu? llista))
  (newline)

  ; Filtrar números múltiples de tres
  (display "Nombres múltiples de tres: ")
  (display (filter multiples-de-tres? llista))
  (newline)

  ; Filtrar números que sean positivos y pares
  (display "Nombres positius i parells: ")
  (display (filter parell? (filter positiu? llista)))
  (newline))
