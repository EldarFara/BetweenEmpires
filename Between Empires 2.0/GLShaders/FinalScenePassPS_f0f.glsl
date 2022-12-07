
varying float2 Tex;

void main()
{
	gl_FragColor = FinalScenePassPS(false, 0, false, Tex);
}
