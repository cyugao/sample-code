import java.util.ArrayList;
import java.util.Arrays;

import edu.princeton.cs.algs4.In;
import edu.princeton.cs.algs4.StdOut;
import edu.princeton.cs.algs4.StdDraw;


public class BruteCollinearPoints {

    private ArrayList<LineSegment> segs = new ArrayList<>();

    public BruteCollinearPoints(Point[] points) {
        if (points == null) throw new IllegalArgumentException();
        int n = points.length;
        // check if any point is null
        for (int j = 0; j < n; j++) {
            if (points[j] == null) throw new IllegalArgumentException();
        }
        Point[] myPoints = points.clone();
        Arrays.sort(myPoints);

        double[][] slopes = new double[n][n];


        // check if there are duplicates
        for (int i = 0; i < n - 1; i++) {
            Point p = myPoints[i];
            for (int j = i + 1; j < n; j++) {
                double slope = p.slopeTo(myPoints[j]);
                if (slope == Double.NEGATIVE_INFINITY) {
                    throw new IllegalArgumentException();
                }
                slopes[i][j] = slope;
            }
        }

        if (n < 4) return;
        for (int i = 0; i < n - 3; i++) {
            Point p = myPoints[i];
            for (int j = i + 1; j < n - 2; j++) {
                double k1 = slopes[i][j];
                for (int k = j + 1; k < n - 1; k++) {
                    double k2 = slopes[i][k];
                    if (k1 != k2) continue;
                    for (int l = k + 1; l < n; l++) {
                        Point s = myPoints[l];
                        double k3 = slopes[i][l];
                        if (k1 == k3) {
                            segs.add(new LineSegment(p, s));
//                            System.out.println(i+" "+j+" "+k+" "+l+" ");
                        }
                    }
                }
            }
        }
//        System.out.println(points[0]);
//        System.out.println(points[4]);

    }    // finds all line segments containing 4 points


    public int numberOfSegments() {
        return segs.size();
    }        // the number of line segments


    public LineSegment[] segments() {
        return segs.toArray(new LineSegment[0]);
    }               // the line segments

    public static void main(String[] args) {

        // read the n points from a file
        In in = new In(args[0]);
        int n = in.readInt();
        Point[] points = new Point[n];
        for (int i = 0; i < n; i++) {
            int x = in.readInt();
            int y = in.readInt();
            points[i] = null;
        }

        boolean draw = false;

        // draw the points
        if (draw) {
            StdDraw.enableDoubleBuffering();
            StdDraw.setXscale(0, 32768);
            StdDraw.setYscale(0, 32768);
            for (Point p : points) {
                p.draw();
            }
            StdDraw.show();
        }

        // print and draw the line segments
        BruteCollinearPoints collinear = new BruteCollinearPoints(points);
        for (LineSegment segment : collinear.segments()) {
            StdOut.println(segment);
            if (draw) segment.draw();
        }
        if (draw) StdDraw.show();
    }
}

