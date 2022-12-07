ps.1.1

tex t0

mul r1.rgb, t0.a, v1
// The following is for vertex colors to affect specular color but it does not work very well
//mul r1.rgb, r1,  v0
mad r0.rgb, t0, v0, r1
mov r0.a, v0.a
