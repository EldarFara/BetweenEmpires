
varying float2 TC;
varying float Depth;

const float alpha_ref_ez = 8.0 / 255.0;

void main()
{
	float alpha = texture2D(MeshTextureSampler, TC).a;
	if((alpha - alpha_ref_ez) < 0.0)
		discard;
	gl_FragColor = vec4(Depth);
}
