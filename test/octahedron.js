// Use a class to store an (x,y,z) coordinate
class Point {
    constructor(x,y,z) {
        this.x = x;
        this.y = y;
        this.z = z;
    }

    // Euclidean distance between two points
    distance(b) { return Math.sqrt(this.dot(b));}

    // Euclidean normal of a point
    norm(b) { 
      return Math.sqrt(this.dot(this));
    }

    cross(b) { // Cross product
      var x = this.y*b.z - this.z*b.y;
      var y = this.z*b.x - this.x*b.z;
      var z = this.x*b.y - this.y*b.x;
      return new Point(x, y, z)
    }

    dot(b) { // Dot product
      return this.x * b.x + this.y * b.y + this.z * b.z;
    }

    plus(b) { // Addition of two points
      return new Point(this.x+b.x, this.y+b.y, this.z+b.z);
    }

    minus(b) { // Subtraction of two points
      return this.plus(b.times(new Point(-1,-1,-1)));
    }

    times(b) { // Multiplication of two points
      return new Point(this.x*b.x, this.y*b.y, this.z*b.z);
    }

    divide(b) { // Division of two points, handles divison by 0
      return new Point(b.x==0 ? 0 : this.x/b.x, b.y==0 ? 0 : this.y/b.y, b.z==0 ? 0 : this.z/b.z);
    }
}

(function() {
    var _onload = function() {
      var pretag = document.getElementById('d'); // The asciiframe
      var tmr1 = undefined; // Used to pause the animation
      // var A=1, B=1;
      
      var intersectRay=function(ray) {
        // Octahedron is unit octahedron centered at (0,0,0)
        // so translate it away from camera at (0,0,0)
        var translation = new Point(0,0,3)

        // Light source position
        var light = new Point(-8,4,0)

        var char = " ";
        // also could store z value to check all faces against

        // Each triangle that makes up an octahedron
        var face1 = [new Point(1,0,0), new Point(0,-1,0), new Point(0,0,1)]; // top tri with +x, +z
        var face2 = [new Point(1,0,0), new Point(0,1,0), new Point(0,0,1)]; // bottom tri with +x, +z
        var face3 = [new Point(-1,0,0), new Point(0,-1,0), new Point(0,0,1)]; // top tri with -x, +z
        var face4 = [new Point(-1,0,0), new Point(0,1,0), new Point(0,0,1)]; // bottom tri with -x, +z
        var face5 = [new Point(-1,0,0), new Point(0,-1,0), new Point(0,0,-1)]; // top tri with -x, -z
        var face6 = [new Point(-1,0,0), new Point(0,1,0), new Point(0,0,-1)]; // bottom tri with -x, -z
        var face7 = [new Point(1,0,0), new Point(0,-1,0), new Point(0,0,-1)]; // top tri with +x, -z
        var face8 = [new Point(1,0,0), new Point(0,1,0), new Point(0,0,-1)]; // bottom tri with +x, -z
        // All of the triangles to loop through
        var faces = [face1, face2, face3, face4, face5, face6, face7, face8];

        faces.forEach(face => {
          // Each vertex of face/triangle of intersection translated then scaled
          var A = face[0].plus(translation)//.times(scale);
          var B = face[1].plus(translation)//.times(scale);
          var C = face[2].plus(translation)//.times(scale);

          // Normal of the plane of intersection
          // (of this face of the octahedron)
          var n = (B.minus(A)).cross(C.minus(A));
          n = n.divide(new Point(n.norm(), n.norm(), n.norm())); // Make it a unit vector

          // The plane of intersection
          // (Normal dotted with any point in a plane)
          var d = n.dot(A);

          // Solve for t, ray = point + t*direction

          var t = d-n.dot(ray)/n.dot(ray)

          // If the intersection is in front of us
          if(t > 0) {
            var hitPoint = ray.plus(ray.times(new Point(t,t,t)));
            // Check if within the triangle region
            // For each edge, AB, AC, CB
            // the cross product of edge and point with vertex
            // should point in the same direction as the normal
            // so
            // ((B-A)x(hit-A).n >= 0)
            // ((C-B)x(hit-B).n >= 0)
            // ((A-C)x(hit-C).n >= 0)
            // and if all three are true then ray hits within face/triangle
            // (= to include the edges)
            if ((B.minus(A)).cross(hitPoint.minus(A)).dot(n) >= 0
              && (C.minus(B)).cross(hitPoint.minus(B)).dot(n) >= 0
              && (A.minus(C)).cross(hitPoint.minus(C)).dot(n) >= 0) {
              // Ray hits, calculate how bright it is here
              var N = 0|8*hitPoint.distance(light)
              char =  ".,-~:;=!*#$@"[N>0?N:0];
            }
          }
        });
        return char;
      };
    
      // This uses the rendering method from https://www.a1k0n.net/2011/07/20/donut-math.html
      // with a full ray tracing method for an octahedron
      var draw=function() {
        // Values for the size of the ascii frame
        var width = 40;
        var height = 21; // One more so it has a row of all newlines

        // for now just get it to render a single frame :L
        // These will allow us to rotate it around a bunch in different axis directions
        // A += 0.07;
        // B += 0.03;

        var buffer=[]; //frame buffer

        // 2D screen that the 3D object is projected onto
        var bound = 1
        var screen_z = 1
        var x_step = 2 * bound/width;
        var y_step = 2 * bound/height;
        var top_left = new Point(-bound-x_step, bound, screen_z)

        var point = top_left

        // For each pixel/ascii in the <pre> we want to draw
        // find what character is there, then put it on the page
        for(var index=0; index<width*height; index++) {
          // Increment x by 1
          point = new Point(point.x += x_step, point.y, point.z)
          if(index%width==0) { // Increase y by 1 at end of row
            buffer[index] = "\n";
            point = new Point(top_left.x,point.y -= y_step, point.z);
          } else {
            buffer[index] = intersectRay(point);
          }
        }
        pretag.innerHTML = buffer.join("");
      };
    
      //
      window.anim = function() {
        if(tmr1 === undefined) {
          tmr1 = setInterval(draw, 50);
        } else {
          clearInterval(tmr1);
          tmr1 = undefined;
        }
      };
      draw();
      // anim(); // This will default to on, Click to toggle off.
    };
    
    if(document.all)
      window.attachEvent('onload',_onload);
    else
      window.addEventListener("load",_onload,false);
    })();
    