
varying float2 Tex;

void main()
{
	gl_FragColor = ps_main_brightPass(true, Tex);
}
