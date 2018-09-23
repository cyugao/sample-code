import edu.princeton.cs.algs4.In;
import edu.princeton.cs.algs4.Point2D;
import edu.princeton.cs.algs4.RectHV;
import edu.princeton.cs.algs4.Stack;
import edu.princeton.cs.algs4.StdDraw;

public class KdTree {

    private int size;
    private Node root;
    private Node champion;
    private double minDistSquared;

    private static class Node {
        private final Point2D p;      // the point
        private final RectHV rect;    // the axis-aligned rectangle corresponding to this node
        private Node lb;        // the left/bottom subtree
        private Node rt;        // the right/top subtree

        public Node(Point2D p, RectHV rect) {
            this.p = p;
            this.rect = rect;
        }
    }

    public KdTree() {
    }

    // construct an empty set of points
    public boolean isEmpty() {
        return size == 0;
    }                      // is the set empty?

    public int size() {
        return size;
    }                         // number of points in the set

    public void insert(Point2D p) {
        if (p == null) throw new IllegalArgumentException();
        root = put(root, p, false, 0, 0, 1, 1);
    }              // add the point to the set (if it is not already in the set)

    private Node put(Node node, Point2D p, boolean horizontal, double x1, double y1, double x2, double y2) {
        boolean less;
        if (node == null) {
            size++;
            return new Node(p, new RectHV(x1, y1, x2, y2));
        }

        // 4 cases
        if (p.equals(node.p)) return node;
        if (horizontal) {
            less = p.y() < node.p.y();
            if (less) node.lb = put(node.lb, p, !horizontal, x1, y1, x2, node.p.y()); // down
            else node.rt = put(node.rt, p, !horizontal, x1, node.p.y(), x2, y2);
        } else {
            less = p.x() < node.p.x();

            if (less) node.lb = put(node.lb, p, !horizontal, x1, y1, node.p.x(), y2); // left
            else node.rt = put(node.rt, p, !horizontal, node.p.x(), y1, x2, y2); // right
        }
        return node;
    }

    public boolean contains(Point2D p) {
        if (p == null) throw new IllegalArgumentException();
        return get(root, p, false);
    }            // does the set contain point p?

    private boolean get(Node x, Point2D p, boolean horizontal) {
        if (x == null) return false;
        if (p.equals(x.p)) return true;
        boolean less;
        if (horizontal) less = p.y() < x.p.y();
        else less = p.x() < x.p.x();
        if (less) return get(x.lb, p, !horizontal);
        else return get(x.rt, p, !horizontal);
    }

    public void draw() {
        draw(root, false);
    }                         // draw all points to standard draw

    private void draw(Node x, boolean horizontal) {
        if (x == null) return;
        StdDraw.setPenColor(StdDraw.BLACK);
        StdDraw.setPenRadius(0.01);
        x.p.draw();
        if (horizontal) {
            StdDraw.setPenColor(StdDraw.GREEN);
            StdDraw.setPenRadius();
            StdDraw.line(x.rect.xmin(), x.p.y(), x.rect.xmax(), x.p.y());
        } else {
            StdDraw.setPenColor(StdDraw.RED);
            StdDraw.setPenRadius();
            StdDraw.line(x.p.x(), x.rect.ymin(), x.p.x(), x.rect.ymax());
        }
        draw(x.lb, !horizontal);
        draw(x.rt, !horizontal);
    }

    public Iterable<Point2D> range(RectHV rect) {
        if (rect == null) throw new IllegalArgumentException();
        Stack<Point2D> pts = new Stack<>();
        Stack<Node> stack = new Stack<>();
        stack.push(root);
        while (!stack.isEmpty()) {
            Node node = stack.pop();
            if (node == null) continue;
            if (rect.intersects(node.rect)) {
                if (rect.contains(node.p)) {
                    pts.push(node.p);
                }
                stack.push(node.lb);
                stack.push(node.rt);
            }
        }
        return pts;
    }             // all points that are inside the rectangle (or on the boundary)

    public Point2D nearest(Point2D p) {
        if (p == null) throw new IllegalArgumentException();
        if (isEmpty()) return null;
        champion = null;
        minDistSquared = Double.POSITIVE_INFINITY;
        search(root, p, false);
        return champion.p;
    }             // a nearest neighbor in the set to point p; null if the set is empty

    private void search(Node node, Point2D p, boolean horizontal) {
        if (node == null) return;
        double dist = p.distanceSquaredTo(node.p);
        if (dist < minDistSquared) {
            minDistSquared = dist;
            champion = node;
        }
        boolean flag;
        if (horizontal) flag = p.y() < node.p.y();
        else flag = p.x() < node.p.x();
        if (flag) {
            // search left / bottom first
            search(node.lb, p, !horizontal);
            if (node.rt == null) return;
            if (minDistSquared > node.rt.rect.distanceSquaredTo(p)) // search only when possible
                search(node.rt, p, !horizontal);
        } else {
            // search right / top first
            search(node.rt, p, !horizontal);
            if (node.lb == null) return;
            if (minDistSquared > node.lb.rect.distanceSquaredTo(p)) // search only when possible
                search(node.lb, p, !horizontal);
        }
    }

    public static void main(String[] args) {
        if (args.length > 0) {
            String filename = args[0];
            In in = new In(filename);
            KdTree kdtree = new KdTree();
            while (!in.isEmpty()) {
                double x = in.readDouble();
                double y = in.readDouble();
                Point2D p = new Point2D(x, y);
                kdtree.insert(p);
            }
            Point2D q = kdtree.nearest(new Point2D(0.27, 0.28));
            System.out.println("----");
            System.out.println(q);
        }
//        Point2D p1 = new Point2D(0.7, 0.2);
//        Point2D p2 = new Point2D(0.5, 0.4);
//        Point2D p3 = new Point2D(0.2, 0.3);
//        Point2D p4 = new Point2D(0.4, 0.7);
//        Point2D p5 = new Point2D(0.9, 0.6);
//        KdTree tree = new KdTree();
//        tree.insert(p1);
//        tree.insert(p2);
//        tree.insert(p3);
//        tree.insert(p4);
//        tree.insert(p5);
//        System.out.println(tree.size());
//        Point2D query = new Point2D(0.272, 0.466);
//        StdDraw.setPenRadius(0.02);
//        query.draw();
//        tree.draw();
//        System.out.println(tree.nearest(query));
    }
}
