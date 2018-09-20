import edu.princeton.cs.algs4.Stack;

import java.util.Arrays;

public class Board {

    private int[] tiles;
    private final int n;
    private final int length;
    private int blankNum, blankRow, blankCol;
    private int manhattan;

    public Board(int[][] blocks) {
        if (blocks == null) {
            throw new IllegalArgumentException();
        }
        n = blocks.length;
        length = n * n;
        tiles = new int[length];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                tiles[n * i + j] = blocks[i][j];
            }
        }

        for (int i = 0; i < length; i++) {
            if (tiles[i] == 0) {
                blankNum = i;
                blankCol = i % n;
                blankRow = i / n;
                break;
            }
        }
        updateManhattan();
    }           // construct tiles board from an n-by-n array of blocks
    // (where blocks[i][j] = block in row i, column j)

    private Board(Board b) {
        tiles = b.tiles.clone();
        n = b.n;
        length = b.length;
        blankNum = b.blankNum;
        blankCol = b.blankCol;
        blankRow = b.blankRow;
    }

    private void swap(int i, int j) {
        int temp = tiles[i];
        tiles[i] = tiles[j];
        tiles[j] = temp;
        updateManhattan();
    }

    public int dimension() {
        return n;
    }                  // board dimension n

    public int hamming() {
        int count = 0;
        for (int i = 0; i < length; i++) {
            if (tiles[i] != i + 1) {
                count++;
            }
        }
        count--;
        return count;
    }                   // number of blocks out of place

    private void updateManhattan() {
        manhattan = 0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                int num = tiles[n * i + j];
                if (num == 0) {
                    continue;
                } else {
                    num = num - 1;
                    int numRow = num / n;
                    int numCol = num % n;
                    manhattan += Math.abs(numRow - i) + Math.abs(numCol - j);
                }
            }
        }
    }

    public int manhattan() {
        return manhattan;
    }                 // sum of Manhattan distances between blocks and goal

    public boolean isGoal() {
        for (int i = 0; i < length - 1; i++) {
            if (tiles[i] != i + 1) {
                return false;
            }
        }
        return true;
    }                // is this board the goal board?

    public Board twin() {
        Board b = new Board(this);
        int i = 0, j = 1;
        if (blankNum == 0) {
            i = 2;
        } else if (blankNum == 1) {
            j = 2;
        }
        b.swap(i, j);
        return b;
    }                    // tiles board that is obtained by exchanging any pair of blocks

    public boolean equals(Object y) {
        if (y == this) return true;
        if (y == null) return false;
        if (y.getClass() != this.getClass()) return false;
        Board that = (Board) y;
        return Arrays.equals(tiles, that.tiles);
    }        // does this board equal y?

    public Iterable<Board> neighbors() {
        Stack<Board> s = new Stack<>();
        // up
        if (blankRow != 0) {
            Board temp = new Board(this);
            temp.swap(temp.blankNum, temp.blankNum - n);
            temp.blankNum -= n;
            temp.blankRow -= 1;
            s.push(temp);
        }
        // down
        if (blankRow != n - 1) {
            Board temp = new Board(this);
            temp.swap(temp.blankNum, temp.blankNum + n);
            temp.blankNum += n;
            temp.blankRow += 1;
            s.push(temp);
        }
        // left
        if (blankCol != 0) {
            Board temp = new Board(this);
            temp.swap(temp.blankNum, temp.blankNum - 1);
            temp.blankNum -= 1;
            temp.blankCol -= 1;
            s.push(temp);
        }
        // right
        if (blankCol != n - 1) {
            Board temp = new Board(this);
            temp.swap(temp.blankNum, temp.blankNum + 1);
            temp.blankNum += 1;
            temp.blankCol += 1;
            s.push(temp);
        }
        return s;
    }     // all neighboring boards


    public String toString() {
        StringBuilder s = new StringBuilder();
        s.append(n + "\n");
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                s.append(String.format("%2d ", tiles[i * n + j]));
            }
            s.append("\n");
        }
        return s.toString();
    }               // string representation of this board (in the output format specified below)


    public static void main(String[] args) {
//        int[][] init = {{8, 0, 3}, {4, 1, 2}, {7, 6, 5}};
//        int[][] init = {{1, 2, 3}, {4, 0, 6}, {7, 5, 8}};
        int[][] init = {{0, 1, 3}, {4, 2, 5}, {7, 8, 6}};
        Board b = new Board(init);
        System.out.println(b.hamming());
        System.out.println(b.manhattan());
        System.out.printf("%d: (%d,%d)\n", b.blankNum, b.blankRow, b.blankCol);
        System.out.println(b);
        System.out.println("-----");
//        System.out.println(b.twin());
//        for (Board bb :
//                b.neighbors()) {
//            System.out.println(bb);
//        }
    } // unit tests (not graded)

}
