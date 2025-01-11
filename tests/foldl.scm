; Implementa foldl
; foldl(f, z, [x1, x2, ..., xn]) = f(...(f(f(z, x1), x2)...), xn)
(define (foldl f acc llista)
  (if (null? llista)
      acc
      (foldl f (f acc (car llista)) (cdr llista))))

; Funciones para usar con foldl
(define (sumar x y)
  (+ x y))

(define (multiplicar x y)
  (* x y))

(define (main)
  ; Lista predefinida para sumar
  (define llista-suma '(1 2 3 4 5))
  (display "Llista de números per sumar: ")
  (display llista-suma)
  (newline)
  (display "Suma de la llista: ")
  (display (foldl sumar 0 llista-suma))
  (newline)

  ; Lista predefinida para multiplicar
  (define llista-producte '(2 3 4))
  (display "Llista de números per multiplicar: ")
  (display llista-producte)
  (newline)
  (display "Producte de la llista: ")
  (display (foldl multiplicar 1 llista-producte))
  (newline))