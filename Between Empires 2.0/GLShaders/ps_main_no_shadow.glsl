
varying vec3 outNormal;
varying vec4 outColor0;
varying vec4 outColor1;
varying vec2 outTexCoord;
varying float outFog;

void main()
{
	float4 tex_col = texture2D(diffuse_texture, outTexCoord);
	INPUT_TEX_GAMMA(tex_col.rgb);
	vec4 finalColor = outColor0 * tex_col;
	
	if(ALPHA_TEST_ENABLED && (finalColor.a - alpha_test_val) < 0.0)
		discard;
		
	OUTPUT_GAMMA(finalColor.rgb);
	
	finalColor.rgb = lerp(vFogColor.rgb, finalColor.rgb, outFog);
	
	gl_FragColor = finalColor;
}
