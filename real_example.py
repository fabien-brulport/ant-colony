import matplotlib.pyplot as plt
from geopy import geocoders
from mpl_toolkits.basemap import Basemap
from geopy.exc import GeocoderTimedOut

from solver.graph import Node, Graph
from solver.aco import ACO


def do_geocode(address, geolocator):
    try:
        return geolocator.geocode(address)
    except GeocoderTimedOut:
        return do_geocode(address, geolocator)


def main():
    # Retrieve cities coordinates and plot (may take some time)
    cities = ['Amsterdam', 'Athens', 'Belfast', 'Belgrade', 'Berlin', 'Bern', 'Brussels', 'Bucharest', 'Budapest',
              'Copenhagen', 'Dublin', 'Helsinki', 'Kiev', 'Lisbon', 'Ljubljana', 'London', 'Luxembourg', 'Madrid', 'Oslo',
              'Paris',
              'Prague', 'Reykjavík', 'Riga', 'Rome', 'Sofia', 'Tallinn', 'Vienna', 'Vilnius', 'Warsaw', 'Zagreb']
    geolocator = geocoders.ArcGIS()
    latitudes = []
    longitudes = []

    for city in cities:
        geo = do_geocode(city, geolocator)
        latitudes.append(geo.latitude)
        longitudes.append(geo.longitude)

    def plot_map(ax):
        basemap = Basemap(projection='mill', llcrnrlon=min(longitudes) - 1, urcrnrlon=max(longitudes) + 1,
                          llcrnrlat=min(latitudes) - 1, urcrnrlat=max(latitudes) + 1, resolution='i', ax=ax)
        basemap.drawcoastlines()
        basemap.fillcontinents()
        basemap.drawmapboundary()
        basemap.drawcountries()
        return basemap

    fig, ax = plt.subplots()
    basemap = plot_map(ax)
    x, y = basemap(longitudes, latitudes)
    basemap.scatter(x, y, marker='o', zorder=2)
    plt.show()

    # Create the graph
    nodes = []
    for i in range(len(cities)):
        nodes.append(Node(x[i], y[i]))

    graph = Graph(nodes)

    # Solve for 100 iterations
    aco = ACO(nodes)
    paths, distances = aco.solve(rho=0.5, n_iterations=100, verbose=True)

    # Plot results
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    basemap = plot_map(axs[0])
    x, y = basemap(longitudes, latitudes)
    basemap.scatter(x, y, marker='o', zorder=2)

    anim = graph.plot_paths(paths, aco.pheromones, distances, fig)
    plt.show()


if __name__ == '__main__':
    main()
