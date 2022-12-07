
varying vec4 outColor0;
varying vec2 outTexCoord;



void main()
{ 
	vec4 finalColor = outColor0;
	finalColor *= texture2D(MeshTextureSampler, outTexCoord);
	gl_FragColor = finalColor;
}