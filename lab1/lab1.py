def main():
    print("Замена последнего элемента каждой строки матрицы на сумму предыдущих элементов этой же строки")

    #Ввод размерности матрицы
    while True:
        try:
            rows_count = int(input("Введите количество строк матрицы: "))
            cols_count = int(input("Введите количество столбцов матрицы: "))
            
            if rows_count <= 0 or cols_count <= 0:
                print("Некорректный формат размерности, повторите ввод")
                continue
            
            if cols_count < 2:
                print("Для работы нужно как минимум 2 столбца, повторите ввод")
                continue
                
            break

        except ValueError:
            print("Введите целое число")

    #Ввод элементов
    matrix = []
    print("Введите элементы матрицы:")
    
    for rowIndex in range(rows_count):
        row = []
        for columnIndex in range(cols_count):
            while True:
                try:
                    val = float(input(f"Строка {rowIndex + 1} элемент {columnIndex + 1}: "))
                    row.append(val)

                    break

                except ValueError:
                    print("Введите числовое значение")

        matrix.append(row)

    print("Введенная матрица:")
    for row in matrix:
        print(row)


    #Замена последнего элемента каждой строки на сумму элементов до него
    resultMatrix = matrix.copy()

    for rowIndex in range(rows_count):
        row_sum = sum(matrix[rowIndex][:-1]) #Сумма среза всех кроме последнего элементов ряда
        resultMatrix[rowIndex][-1] = row_sum #Кладем в последний элемент каждой строки

    #Вывод результата
    print("Матрица после замены последних элементов:")
    for row in resultMatrix:
        print(row)

if __name__ == "__main__":
    main()