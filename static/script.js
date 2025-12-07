// No need for a full URL anymore, relative paths work!
const GENERATE_ENDPOINT = "/generate-midi"; 

const generateBtn = document.getElementById('generateBtn');
const downloadBtn = document.getElementById('downloadBtn');
const player = document.getElementById('myPlayer');
const statusText = document.getElementById('statusText');

generateBtn.addEventListener('click', async () => {
    generateBtn.disabled = true;
    generateBtn.innerText = "Generating...";
    statusText.innerText = "Consulting the AI model...";
    downloadBtn.classList.add('disabled');

    try {
        // Fetch using relative path
        const response = await fetch(GENERATE_ENDPOINT);
        
        if (!response.ok) throw new Error("Generation failed");

        const blob = await response.blob();
        const midiUrl = URL.createObjectURL(blob);

        player.src = midiUrl;
        
        downloadBtn.href = midiUrl;
        downloadBtn.download = `ai-song-${Date.now()}.mid`;
        downloadBtn.classList.remove('disabled');
        
        statusText.innerText = "Song generated successfully!";

    } catch (error) {
        console.error(error);
        statusText.innerText = "Error generating song.";
    } finally {
        generateBtn.disabled = false;
        generateBtn.innerText = "Generate New Song";
    }
});