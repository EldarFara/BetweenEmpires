
varying float2 Tex;

void main()
{
	gl_FragColor = ps_main_postFX_DofBlur(false, true, Tex);
}
