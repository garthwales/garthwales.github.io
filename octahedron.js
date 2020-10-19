// Use a class to store an (x,y,z) coordinate
class Point {
    constructor(x,y,z) {
        this.x = x;
        this.y = y;
        this.z = z;
    }

    norm(b) {
      return Math.sqrt(this.dot(this));
    }

    cross(b) {
      var x = this.y*b.z - this.z*b.y;
      var y = this.z*b.x - this.x*b.z;
      var z = this.x*b.y - this.y*b.x;
      return new Point(x, y, z)
    }

    dot(b) {
      return this.x * b.x + this.y * b.y + this.z * b.z;
    }

    plus(b) {
      return new Point(this.x+b.x, this.y+b.y, this.z+b.z);
    }

    minus(b) {
      return this.plus(b.times(new Point(-1,-1,-1)));
    }

    times(b) {
      return new Point(this.x*b.x, this.y*b.y, this.z*b.z);
    }

    divide(b) {
      return new Point(b.x==0 ? 0 : this.x/b.x, b.y==0 ? 0 : this.y/b.y, b.z==0 ? 0 : this.z/b.z);
    }
}

// (function() {
//     var _onload = function() {
//       var pretag = document.getElementById('d');
    
//       var tmr1 = undefined;
//       var A=1, B=1;
    
      // This uses the rendering method from https://www.a1k0n.net/2011/07/20/donut-math.html
      // with a full ray tracing method for an octahedron
      var asciiframe=function() {
        var width = 40;
        var height = 40;
        var step = 1;

        var scale = new Point(5,5,5); // Make it 2x bigger than the default
        var translation = new Point(0,0,4); // Move it 3 in the z (away from camera)

        var camera = new Point(0,0,0)

        // for now just get it to render a single frame :L
        // These will allow us to rotate it around a bunch in different axis directions
        // A += 0.07;
        // B += 0.03;

        var buffer=[]; //frame buffer
        var z=[]; //z-buffer

        var w_limit = width/step;
        var h_limit = height/step;

        var top_left = new Point(-w_limit-step, h_limit, 2)
        var point = top_left


        var face1 = [new Point(1,0,0), new Point(0,-1,0), new Point(0,0,1)]; // top tri with +x, +z
        var face2 = [new Point(1,0,0), new Point(0,1,0), new Point(0,0,1)]; // bottom tri with +x, +z
        var face3 = [new Point(-1,0,0), new Point(0,-1,0), new Point(0,0,1)]; // top tri with -x, +z
        var face4 = [new Point(-1,0,0), new Point(0,1,0), new Point(0,0,1)]; // bottom tri with -x, +z
        var face5 = [new Point(-1,0,0), new Point(0,-1,0), new Point(0,0,-1)]; // top tri with -x, -z
        var face6 = [new Point(-1,0,0), new Point(0,1,0), new Point(0,0,-1)]; // bottom tri with -x, -z
        var face7 = [new Point(1,0,0), new Point(0,-1,0), new Point(0,0,-1)]; // top tri with +x, -z
        var face8 = [new Point(1,0,0), new Point(0,1,0), new Point(0,0,-1)]; // bottom tri with +x, -z

        var faces = [face1, face2, face3, face4, face5, face6, face7, face8];


        for(var index=0; index<width*height; index++) {
          // Increment x by step
          point = new Point(point.x += step, point.y, point.z)
          if(index%w_limit==0) { // Increase y by step at end of row
            buffer[index] = "\n";
            point = new Point(top_left.x,point.y-=step, point.z);
          } else {
            buffer[index] = " ";
          }
          
          // Direction the ray is traveling in
          var dX = point.x/point.z;
          var dY = point.y/point.z;
          var dZ = 0;

          var direction = new Point(dX, dY, dZ)

          faces.forEach(face => {
            // Each vertex of face/triangle of intersection translated then scaled
            var A = face[0].plus(translation).times(scale);
            var B = face[1].plus(translation).times(scale);
            var C = face[2].plus(translation).times(scale);

            // Normal of the plane of intersection
            // (of this face of the octahedron)
            var n = (B.minus(A)).cross(C.minus(A));
            n = n.divide(n.norm()); // Make it a unit vector

            // The plane of intersection
            // (Normal dotted with any point in a plane)
            var d = n.dot(A);

            // Solve for t, ray = point + t*direction
            var t = (d-(n.dot(point)))/(n.dot(direction))

            // If the intersection is in front of us
            if(t > 0) {
              var hitPoint = point.plus(direction.times(new Point(t,t,t)));
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
                buffer[index] = "&";
                // The ray hits the face
                // Calculate the

                // if(n.dot(direction) > 0) {
                //   n = n.times(new Point(-1,-1,-1));
                // }

              }

            }

          });


        }
        console.log(buffer);

        // var b=[]; // Buffer of pixels
        // var z=[]; // Z-buffer of each pixel
        // var cA=Math.cos(A), sA=Math.sin(A),
        //     cB=Math.cos(B), sB=Math.sin(B);
        // for(var k=0;k<1760;k++) {
        //   b[k]=k%80 == 79 ? "\n" : " ";
        //   z[k]=0;
        // }

        // Screen at z1 distance from view.
        // octahedron at z1+z1 distance (at center)
        
        // Check if a ray traced point intersects with the triangles located at:
        // face1 = {Point(1,0,0), Point(0,-1,0), Point(0,0,1)}; // top tri with +x, +z
        // face2 = {Point(1,0,0), Point(0,1,0), Point(0,0,1)}; // bottom tri with +x, +z
        // face3 = {Point(-1,0,0), Point(0,-1,0), Point(0,0,1)}; // top tri with -x, +z
        // face4 = {Point(-1,0,0), Point(0,1,0), Point(0,0,1)}; // bottom tri with -x, +z
        // face5 = {Point(-1,0,0), Point(0,-1,0), Point(0,0,-1)}; // top tri with -x, -z
        // face6 = {Point(-1,0,0), Point(0,1,0), Point(0,0,-1)}; // bottom tri with -x, -z
        // face7 = {Point(1,0,0), Point(0,-1,0), Point(0,0,-1)}; // top tri with +x, -z
        // face8 = {Point(1,0,0), Point(0,1,0), Point(0,0,-1)}; // bottom tri with +x, -z

        // for each triangle:
        // calculate the same as in Octahedron.cpp

        // Also, will want to have a scale factor + translate(x,y,z) values for stock object

        // { do the calculation here}




    //     pretag.innerHTML = b.join("");
      };
      asciiframe();
    
    //   window.anim1 = function() {
    //     if(tmr1 === undefined) {
    //       tmr1 = setInterval(asciiframe, 50);
    //     } else {
    //       clearInterval(tmr1);
    //       tmr1 = undefined;
    //     }
    //   };
    //   asciiframe();
    //   anim1(); // This means it will start on. Click to toggle off.
    // }
    
    // if(document.all)
    //   window.attachEvent('onload',_onload);
    // else
    //   window.addEventListener("load",_onload,false);
    // })();
    