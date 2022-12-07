
varying float2 Tex;

void main()
{
	float original_shadowmap = texture2D(postFX_sampler0, Tex).r;
	float character_shadow = texture2D(postFX_sampler1, Tex).r;
	
	gl_FragColor = vec4(min(original_shadowmap, character_shadow));
}
