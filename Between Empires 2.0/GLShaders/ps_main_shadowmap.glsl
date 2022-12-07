
varying vec3 outNormal;
varying vec4 outColor0;
varying vec4 outColor1;
varying vec2 outTexCoord;
varying float outDepth;



void main()
{ 
	vec4 finalColor;
	finalColor.a = texture2D(MeshTextureSampler, outTexCoord).a;
	finalColor.a -= 0.5;
	
	if (finalColor.a < 0.0)
		discard;
	
	finalColor.rgba = vec4(outDepth);// + fShadowBias;

	gl_FragColor = finalColor;
}