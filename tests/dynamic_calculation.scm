(define (sumar-dos-valors)
  (display "Introdueix el primer valor: ")
  (let ((x (read)))
    (display "Introdueix el segon valor: ")
    (let ((y (read)))
      (display "La suma és: ")
      (display (+ x y))
      (newline)
      (display "El producte és: ")
      (display (* x y))
      (newline)
      (display "El quocient és: ")
      (if (= y 0)
          (display "Indefinit (divisió per zero)")
          (display (/ x y)))
      (newline))))

(define (main)
  (sumar-dos-valors))