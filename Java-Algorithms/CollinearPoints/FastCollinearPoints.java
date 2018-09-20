import edu.princeton.cs.algs4.In;
import edu.princeton.cs.algs4.StdDraw;
import edu.princeton.cs.algs4.StdOut;

import java.util.ArrayList;
import java.util.Arrays;


public class FastCollinearPoints {

    private ArrayList<LineSegment> segs = new ArrayList<>();

    public FastCollinearPoints(Point[] points) {
        if (points == null) throw new IllegalArgumentException();
        int n = points.length;
        // check if any point is null
        for (int j = 0; j < n; j++) {
            if (points[j] == null) throw new IllegalArgumentException();
        }
        Point[] myPoints = points.clone();
        Arrays.sort(myPoints);


        // System.out.println();

        // check if there are duplicates
        for (int i = 0; i < n - 1; i++) {
            Point p = myPoints[i];
            for (int j = i + 1; j < n; j++) {
                double slope = p.slopeTo(myPoints[j]);
                if (slope == Double.NEGATIVE_INFINITY) {
                    throw new IllegalArgumentException();
                }
            }
        }

        if (n < 4) return;
        for (int i = 0; i < n; i++) {
            Point p = points[i];
            Arrays.sort(myPoints, p.slopeOrder());
            int count = 1;
            double prevSlope = p.slopeTo(myPoints[1]);
            Point minPt = p.compareTo(myPoints[1]) > 0 ? myPoints[1] : p;
            Point maxPt = myPoints[1];
            for (int j = 2; j < n; j++) {
                double slope = p.slopeTo(myPoints[j]);

                if (slope == prevSlope) {
                    count++;
                } else {
                    if (count >= 3 && minPt == p) {
                        segs.add(new LineSegment(p, maxPt));
                    }
                    count = 1;
                    prevSlope = slope;
                    minPt = p;
                    maxPt = p;
                }
                if (minPt.compareTo(myPoints[j]) > 0) {
                    minPt = myPoints[j];
                }
                if (maxPt.compareTo(myPoints[j]) < 0) {
                    maxPt = myPoints[j];
                }
            }
            if (count >= 3 && minPt == p) {
                segs.add(new LineSegment(p, maxPt));
            }
        }

//        System.out.println(points[0]);
//        System.out.println(points[4]);
//        System.out.println("???" + points[0].slopeTo(points[4]));

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
            points[i] = new Point(x, y);
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
        // System.out.println("Result");
        FastCollinearPoints collinear = new FastCollinearPoints(points);
        for (LineSegment segment : collinear.segments()) {
            StdOut.println(segment);
            if (draw) segment.draw();
        }
        if (draw) StdDraw.show();
    }
}

