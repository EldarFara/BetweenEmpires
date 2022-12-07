
varying vec3 outNormal;
varying vec4 outColor0;
varying vec4 outColor1;
varying vec2 outTexCoord;



void main()
{ 
	float4 tex_col = texture2D(MeshTextureSamplerNoFilter, outTexCoord);
	INPUT_TEX_GAMMA(tex_col.rgb);
	vec4 finalColor = outColor0 * tex_col;
	OUTPUT_GAMMA(finalColor.rgb);
	gl_FragColor = finalColor;
}