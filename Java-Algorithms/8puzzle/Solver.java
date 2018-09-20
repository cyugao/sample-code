import edu.princeton.cs.algs4.MinPQ;
import edu.princeton.cs.algs4.In;
import edu.princeton.cs.algs4.Stack;

public class Solver {

    private boolean solvable;
    private int moves = -1;
    private Node goalNode;
    private final Node nullNode = new Node();

    private class Node implements Comparable<Node> {

        private Board board;
        private int cost;
        private final int moves;
        private Node pred;

        public Node(Board board, Node pred) {
            this.board = board;
            this.moves = pred.moves + 1;
            this.cost = this.moves + board.manhattan();
            this.pred = pred;
        }

        public Node() {
            this.moves = -1;
        }


        @Override
        public int compareTo(Node that) {
            return Integer.compare(this.cost, that.cost);
        }
    }

    public Solver(Board initial) {
        if (initial == null) {
            throw new IllegalArgumentException();
        }
        Node initNode = new Node(initial, nullNode);
        Board dualInitial = initial.twin();
        Node dualInitNode = new Node(dualInitial, nullNode);
        MinPQ<Node> pq = new MinPQ<Node>();
        MinPQ<Node> dualPq = new MinPQ<Node>();
        pq.insert(initNode);
        dualPq.insert(dualInitNode);
        while (true) {
            Node node = pq.delMin();
            Board b = node.board;
            if (b.isGoal()) {
                solvable = true;
                goalNode = node;
                break;
            }
            Node dualNode = dualPq.delMin();
            Board dualB = dualNode.board;
            if (dualB.isGoal()) {
                solvable = false;
                break;
            }
            for (Board nbr : b.neighbors()
            ) {
                if (!nbr.equals(node.pred.board)) {
                    pq.insert(new Node(nbr, node));
                }
            }
            for (Board nbr : dualB.neighbors()
            ) {
                if (!nbr.equals(dualNode.pred.board)) {
                    dualPq.insert(new Node(nbr, dualNode));
                }
            }
        }

        if (solvable) {
            moves = goalNode.moves;
        }
    }           // find a solution to the initial board (using the A* algorithm)

    public boolean isSolvable() {
        return solvable;
    }            // is the initial board solvable?

    public int moves() {
        return moves;
    }                     // min number of moves to solve initial board; -1 if unsolvable

    public Iterable<Board> solution() {
        if (!solvable) return null;
        Stack<Board> sol = new Stack<>();
        Node node = goalNode;

        while (node != nullNode) {
            sol.push(node.board);
            node = node.pred;
        }
        return sol;
    }      // sequence of boards in a shortest solution; null if unsolvable

    public static void main(String[] args) {

        // for each command-line argument
        for (String filename : args) {

            // read in the board specified in the filename
            In in = new In(filename);
            int n = in.readInt();
            int[][] tiles = new int[n][n];
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    tiles[i][j] = in.readInt();
                }
            }

            // solve the slider puzzle
            Board initial = new Board(tiles);
            Solver solver = new Solver(initial);
            if (!solver.isSolvable()) {
                System.out.println("No solution possible");
            } else {
                System.out.println("Minimum number of moves = " + solver.moves());
                System.out.println();
                for (Board b :
                        solver.solution()) {
                    System.out.println(b);
                }
            }
        }
    } // solve a slider puzzle (given below)
}
