(define (map func llista)
  (if (null? llista)
      '()
      (cons (func (car llista)) (map func (cdr llista)))))

(define (dobla x) (* x 2))

(define (sumar-llista llista)
  (if (null? llista)
      0
      (+ (car llista) (sumar-llista (cdr llista)))))

(define (main)
  (let ((llista '(1 2 3 4 5)))
    (display "Llista original: ")
    (display llista)
    (newline)
    (display "Llista doblada: ")
    (display (map dobla llista))
    (newline)
    (display "Suma de la llista doblada: ")
    (display (sumar-llista (map dobla llista)))
    (newline)))