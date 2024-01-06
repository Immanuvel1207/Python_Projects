#include <stdio.h>
#include <stdbool.h>
#define N 9
bool isSafe(int grid[N][N], int row, int col, int num) {
    for (int x = 0; x < N; x++) {
        if (grid[row][x] == num || grid[x][col] == num) {
            return false;
        }
    }
    int startRow = row - row % 3;
    int startCol = col - col % 3;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (grid[i + startRow][j + startCol] == num) {
                return false;
            }
        }
    }
    return true;
}
bool findEmptyCell(int grid[N][N], int* row, int* col) {
    for (*row = 0; *row < N; (*row)++) {
        for (*col = 0; *col < N; (*col)++) {
            if (grid[*row][*col] == 0) {
                return true;
            }
        }
    }
    return false;
}
bool solveSudoku(int grid[N][N]) {
    int row, col;
    if (!findEmptyCell(grid, &row, &col)) {
        return true;}
    for (int num = 1; num <= N; num++) {
        if (isSafe(grid, row, col, num)) {
            grid[row][col] = num;
            if (solveSudoku(grid)) {
                return true;}
            grid[row][col] = 0;
        }
    }
    return false;
}
void printGrid(int grid[N][N]) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            printf("%2d ", grid[i][j]);
        }
        printf("\n");
    }
}
int main() {
    int i, j, grid[N][N];
    printf("Enter the Values row by row (0 if no element)\n");
    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            scanf("%d", &grid[i][j]);
        }
        printf("\n");
    }
    if (solveSudoku(grid)) {
        printf("Sudoku solution:\n");
        printGrid(grid);}
 else {
        printf("No solution exists.\n");}
    return 0;
}
